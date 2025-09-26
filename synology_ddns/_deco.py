#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decorators module

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025/7/1 15:50
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from functools import wraps
from re import sub
from traceback import format_exc
from typing import Callable

from flask import current_app

from ._exceptions import NotFQDNError, RecordNotChangedError, NoResolveForEndpointError
from ._exceptions import OverHeatError, NoHostError, APIError
from ._exceptions import ProviderNotFoundError, ProviderNotSupportedError
from ._exceptions import RequiredParametersNotFoundError, InvalidPasswordError
from ._response import ResponseString as Rs
from ._verify import APIProviders


def sanitize_error_message(message: str) -> str:
    """Remove sensitive information from error messages"""
    # Remove potential API tokens/keys (alphanumeric strings > 20 chars)
    message = sub(r"[A-Za-z0-9_-]{20,}", "[REDACTED]", message)
    # Remove potential passwords in URLs
    message = sub(r"password=[^&\s]+", "password=[REDACTED]", message)
    return message


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
            sanitized_error = sanitize_error_message(str(error))
            current_app.logger.error(sanitized_error)

            # Only log full traceback in debug mode, and sanitize it
            if current_app.debug:
                sanitized_traceback = sanitize_error_message(format_exc())
                current_app.logger.debug(sanitized_traceback)

            try:
                provider = APIProviders.get_provider()
                msg = f"An error occurred when trying to update record, see: {provider.doc}"
                current_app.logger.info(msg)
            except (ProviderNotFoundError, ProviderNotSupportedError):
                ...
            for kind, response in mapper.items():
                if isinstance(error, kind):
                    return response
            raise error  # pragma: no cover

    return wrapper
