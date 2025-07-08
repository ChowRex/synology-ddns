#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Abstract module

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025-07-01 09:26:32
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from abc import ABC, abstractmethod
from re import match, compile as cmp
from socket import gethostbyname_ex, gaierror
from typing import Dict, List
from urllib.parse import urlparse

from flask import current_app

from .._exceptions import NoResolveForEndpointError, RequiredParametersNotFoundError
from .._exceptions import RecordNotChangedError, NotFQDNError
from .._parameters import params
from .._response import ResponseString as Rs

_REQUIRED_ARGS: List[str] = ["hostname", "username", "password"]


class AbstractDDNSProvider(ABC):
    """Abstract DDNS service provider class"""

    # Cache the latest records
    _LATEST_RECORDS: Dict[str, str] = {}

    @abstractmethod
    def _update(self) -> None:
        """
        Subclass must implement this method to update ddns record
        :return: None
        :raises:
            - NoResolveForEndpointError
        """

    @property
    @abstractmethod
    def doc(self) -> str:
        """
        Subclass must implement this method to get doc URL
        :return: Document URL
        """

    @property
    @abstractmethod
    def end_point(self) -> str:
        """
        Subclass must implement this method to get end point
        :return: Endpoint URL
        """

    @staticmethod
    def _verify_arguments() -> None:
        """
        Verify arguments
        :return: None
        :raises: RequiredParametersNotFoundError
        """
        # Verify myip
        if not params.myip:
            msg = "Lack of myip argument"
            current_app.logger.critical(msg)
            raise RequiredParametersNotFoundError(msg)

        for arg in _REQUIRED_ARGS:
            if not getattr(params, arg):
                msg = f"CAN'T get required parameter: {arg} from argument or environment variable"
                current_app.logger.critical(msg)
                raise RequiredParametersNotFoundError(msg)

    @staticmethod
    def _check_fqdn() -> None:
        """
        Check if FQDN is correct

        Refer:
        https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch08s15.html

        :return: None
        :raises: NotFQDNError
        """
        hostname = params.hostname
        regex = cmp(r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$')
        if not match(regex, hostname):
            msg = f"{hostname} is not a valid FQDN"
            current_app.logger.error(msg)
            raise NotFQDNError(msg)

    def _verify_same_record(self) -> None:
        """
        Check if same record
        :return: None
        :raises: RecordNotChangedError
        """
        if self._LATEST_RECORDS.get(params.hostname) == params.myip:
            msg = f"{params.hostname}'s record is not changed"
            current_app.logger.warning(msg)
            raise RecordNotChangedError(msg)

    def _resolve_endpoint(self) -> None:
        """
        Try to resolve endpoint
        :return: None
        :raises: NoResolveForEndpointError
        """
        hostname = urlparse(self.end_point).hostname
        try:
            gethostbyname_ex(hostname)
        except gaierror:
            msg = f"Can't resolve endpoint: {hostname}"
            current_app.logger.critical(msg)
            raise NoResolveForEndpointError(msg) from gaierror

    def update(self) -> str:
        """
        Update ddns record function

        :return: Response string
        :raises:
            - `RequiredParametersNotFoundError`: Lack of key parameter
            - `NotFQDNError`: Hostname is not a valid FQDN
            - `RecordNotChangedError`: Myip is not changed
            - `NoResolveForEndpointError`: Provider endpoint cannot be resolved
        """
        self._verify_arguments()
        self._check_fqdn()
        self._verify_same_record()
        self._resolve_endpoint()
        self._update()
        # Everything works fine, then cache the result and return.
        self._LATEST_RECORDS[params.hostname] = params.myip
        return Rs.OK.value
