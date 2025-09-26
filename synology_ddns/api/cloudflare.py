#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""
CloudFlare API provider, go to `Cloudflare Fundamentals docs`_ for more details.

.. _`Cloudflare Fundamentals docs`: https://developers.cloudflare.com/fundamentals/api/reference/sdks

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025-07-01 09:29:01
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
__all__ = ["CloudFlareDDNS"]

from typing import Union, Dict
from threading import Lock

from cloudflare import APIConnectionError, PermissionDeniedError, InternalServerError
from cloudflare import AuthenticationError, BadRequestError, RateLimitError
from cloudflare import Cloudflare
from flask import current_app

from ._abstract import AbstractDDNSProvider
from .._exceptions import InvalidPasswordError, NoHostError, OverHeatError, APIError
from .._parameters import params

_BadAuthTypes = (
    AuthenticationError,
    BadRequestError,
    PermissionDeniedError,
    InvalidPasswordError,
)


class CloudFlareDDNS(AbstractDDNSProvider):
    """CloudFlare DDNS modifier class"""

    _END_POINT: str = "https://api.cloudflare.com"
    _ENV_ACCOUNT_ID: str = "CLOUDFLARE_ACCOUNT_ID"
    _instance: Union[AbstractDDNSProvider, None] = None
    _initialized: bool = False
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:  # pragma: no cover
            return
        self._make_client = lambda: Cloudflare(api_token=params.password)
        self._client: Union[None, Cloudflare] = None
        # Used to cache the mapping between username and zone id.
        self._zones: Dict[str, str] = {}
        # Used to cache the mapping between hostname and record id.
        self._records: Dict[str, str] = {}

    @property
    def end_point(self) -> str:
        """
        Return the Cloudflare DDNS endpoint URL
        :return: Endpoint URL
        """
        return self._END_POINT

    @property
    def doc(self) -> str:
        """
        Return doc URL
        :return: Document URL
        """
        return self._END_POINT

    def _get_client_by_user_token(self) -> None:
        """
        Try to verify the token through the user token verification function.

        For more information about user token, see: `API token`_

        .. _`API token`: https://developers.cloudflare.com/fundamentals/api/get-started/create-token

        :return: None
        :raise: AuthenticationError, BadRequestError, RateLimitError, InvalidPasswordError
        """
        self._client = self._make_client()
        current_app.logger.debug("Trying to verify password as user token")
        response = self._client.user.tokens.verify()
        if response.status != "active":  # pragma: no cover
            raise InvalidPasswordError
        current_app.logger.info("Successfully verified user API token")

    def _get_client_by_account_token(self) -> None:
        """
        Try to verify the token through the account token verification function.

        For more information about account token, see: `Account token`_

        .. _`Account token`: https://developers.cloudflare.com/fundamentals/api/get-started/account-owned-tokens

        :return: None
        :raise: AuthenticationError, BadRequestError, RateLimitError, InvalidPasswordError
        """
        self._client = self._make_client()
        if not (account_id := params.get(self._ENV_ACCOUNT_ID)):
            msg = f"{params.ENV_PREFIX}_{self._ENV_ACCOUNT_ID}"
            msg = f"CAN'T find account ID from environment variable {msg}"
            current_app.logger.critical(msg)
            raise InvalidPasswordError
        current_app.logger.debug("Trying to verify password as account token")
        response = self._client.accounts.tokens.verify(account_id=account_id)
        if response.status != "active":  # pragma: no cover
            raise InvalidPasswordError
        current_app.logger.info("Successfully verified account API token")

    @property
    def client(self) -> Cloudflare:
        """
        Use the parameter `password` as token and verify that it is valid.

        1. Try to verify the token by :meth:`_get_client_by_user_token`

        2. Try to verify the token by :meth:`_get_client_by_account_token`

        If both methods are failed, raise exception.

        For more information about CloudFlare SDK, see: `CloudFlare SDK`_

        .. _`CloudFlare SDK`: https://github.com/cloudflare/cloudflare-python/blob/main/api.md

        :return: Cloudflare client
        :raises: AuthenticationError, BadRequestError, RateLimitError, InvalidPasswordError
        """
        if self._client is None:
            try:
                self._get_client_by_user_token()
            except _BadAuthTypes:
                self._get_client_by_account_token()
        return self._client

    def _get_zone_id(self) -> str:
        """
        Get zone ID via Cloudflare SDK.
        :return: Zone ID
        """
        if zone_id := self._zones.get(params.username):
            return zone_id
        kwargs = {"name": params.username}
        try:
            zone_id = list(self.client.zones.list(**kwargs))[0].id
            self._zones[params.username] = zone_id
            return zone_id
        except IndexError:
            msg = f"CAN'T find zone from username: {params.username}"
            current_app.logger.critical(msg)
            raise NoHostError(msg) from IndexError

    def _get_record_id(self) -> str:
        """
        Get record ID via Cloudflare SDK.
        :return: Record ID
        """
        if record_id := self._records.get(params.hostname):
            return record_id
        zone_id = self._get_zone_id()
        kwargs = {"zone_id": zone_id, "name": params.hostname}
        try:
            record_id = list(self.client.dns.records.list(**kwargs))[0].id
            self._records[params.hostname] = record_id
            return record_id
        except IndexError:
            msg = f"CAN'T find record from hostname: {params.hostname}"
            current_app.logger.warning(msg)
        return ""

    def _create_record(self, kind: str = "A") -> str:
        """
        Create record via Cloudflare SDK. Then add it into cache.
        :param kind: Type of record
        :return: ID of new record
        """
        kwargs = {
            "zone_id": self._get_zone_id(),
            "name": params.hostname,
            "type": kind,
            "content": params.myip,
        }
        record = self.client.dns.records.create(**kwargs)
        self._records[params.hostname] = record.id
        return record.id

    def _edit_record(self, kind: str = "A") -> None:
        """
        Edit record via Cloudflare SDK.
        :param kind: Type of record
        :return: None
        """
        kwargs = {
            "dns_record_id": self._get_record_id(),
            "zone_id": self._get_zone_id(),
            "name": params.hostname,
            "type": kind,
            "content": params.myip,
        }
        self.client.dns.records.edit(**kwargs)

    def _delete_record(self) -> None:
        """
        Delete record via Cloudflare SDK. Then remove it from cache.
        :return: None
        """
        kwargs = {
            "zone_id": self._get_zone_id(),
            "dns_record_id": self._get_record_id(),
        }
        self.client.dns.records.delete(**kwargs)
        if params.hostname in self._records:
            self._records.pop(params.hostname)

    def _update(self) -> None:
        """
        Cloudflare DDNS update method

        Check if the record id valid?

           - Yes: Try to update record's value via CloudFlare client.
           - No: Try to create a new record and get the record id via CloudFlare client.

        :return: None
        :raises:
            - InvalidPasswordError: Authentication failed
            - OverHeatError: Rate limit exceeded
            - ConnectionError: Connection failed
            - APIError: Internal server error
        """
        try:
            if self._get_record_id():
                self._edit_record()
            else:
                self._create_record()
            # Do post cleanup when the test flag is set.
            if params.get("test"):
                self._delete_record()
        except _BadAuthTypes as error:
            current_app.logger.error(error)
            raise InvalidPasswordError from error
        except RateLimitError as error:  # pragma: no cover
            raise OverHeatError from error
        except APIConnectionError as error:  # pragma: no cover
            current_app.logger.error(error)
            raise ConnectionError from error
        except InternalServerError as error:  # pragma: no cover
            raise APIError from error
