#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API providers module

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025-07-01 09:26:14
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""

from ._abstract import AbstractDDNSProvider
from .cloudflare import CloudFlareDDNS
