#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decorators module

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025/7/1 15:50
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from traceback import format_exc
from functools import wraps
from typing import Callable

from flask import current_app

from ._exceptions import NotFQDNError, RecordNotChangedError, NoResolveForEndpointError
from ._exceptions import ProviderNotFoundError, ProviderNotSupportedError
from ._exceptions import RequiredParametersNotFoundError, InvalidPasswordError
from ._exceptions import OverHeatError, NoHostError, APIError
from ._response import ResponseString as Rs
from ._verify import APIProviders


def handle_exceptions(function: Callable):
    """
    Decorator to handle exceptions
    :param function: Function to decorate
    :return:
    """

    @wraps(function)
    def wrapper():
        """
        Handle exceptions
        :return:
        """
        mapper = {
            # Locale error
            ProviderNotFoundError: Rs.BAD_REQUEST.value,
            ProviderNotSupportedError: Rs.BAD_REQUEST.value,
            RequiredParametersNotFoundError: Rs.BAD_REQUEST.value,
            NotFQDNError: Rs.NOT_FQDN.value,
            RecordNotChangedError: Rs.NO_CHANGE.value,
            NoResolveForEndpointError: Rs.BAD_RESOLVE.value,
            # Remote error
            InvalidPasswordError: Rs.BAD_AUTH.value,
            OverHeatError: Rs.ABUSE.value,
            NoHostError: Rs.NO_HOST.value,
            ConnectionError: Rs.BAD_CONNECTION.value,
            APIError: Rs.API_ERROR.value,
        }
        try:
            return function()
        # pylint: disable=broad-exception-caught
        except Exception as error:
            current_app.logger.error(error)
            current_app.logger.debug(format_exc())
            try:
                provider = APIProviders.get_provider()
                msg = f"An error occurred when trying to update record, see: {provider.doc}"
                current_app.logger.info(msg)
            except (ProviderNotFoundError, ProviderNotSupportedError):
                ...
            for kind, response in mapper.items():
                if isinstance(error, kind):
                    current_app.logger.error(error)
                    return response
            raise error  # pragma: no cover

    return wrapper
