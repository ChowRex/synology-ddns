#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify module

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025/6/30 17:07
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from enum import Enum

from flask import current_app, request

from ._exceptions import ProviderNotFoundError, ProviderNotSupportedError
from .api import AbstractDDNSProvider, CloudFlareDDNS


# pylint: disable=invalid-name
class APIProviders(Enum):
    """Supported API providers"""

    cloud_flare = CloudFlareDDNS

    @classmethod
    def _all_providers(cls) -> dict[str, type[AbstractDDNSProvider]]:
        """
        Return dict of supported API providers
        :return:
        """
        providers = {_.name: _.value for _ in cls}
        return providers

    @classmethod
    def get_provider(cls) -> AbstractDDNSProvider:
        """
        Get a specific API provider.
        :return:
        """
        providers = cls._all_providers()
        provider = request.args.get("api", "")
        if not provider:
            msg = "Must provide a provider name"
            current_app.logger.critical(msg)
            raise ProviderNotFoundError(msg)
        if provider not in providers:
            msg = f"Unsupported API provider: {provider}"
            current_app.logger.critical(msg)
            raise ProviderNotSupportedError(msg)
        instance = providers[provider]()
        return instance
