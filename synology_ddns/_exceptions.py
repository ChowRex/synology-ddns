#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom exceptions module

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025/6/30 17:07
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""


class ProviderNotFoundError(Exception):
    """Provider not found from `request.args` exception"""


class ProviderNotSupportedError(Exception):
    """Provider not supported from `request.args` exception"""


class RequiredParametersNotFoundError(Exception):
    """Lack required parameters exception"""


class NotFQDNError(Exception):
    """Not FQDN exception"""


class RecordNotChangedError(Exception):
    """Record not changed exception"""


class NoResolveForEndpointError(Exception):
    """Endpoint not resolved exception"""


class InvalidPasswordError(Exception):
    """Password invalid exception"""


class NoHostError(Exception):
    """No host exception"""


class OverHeatError(Exception):
    """Overheat exception"""


class APIError(Exception):
    """API error exception"""
