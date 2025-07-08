#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synology DSM DDNS customer provider.

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025/6/30 17:05
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""

__version__ = '0.0.1'

__author__ = 'Rex Zhou'
__copyright__ = 'Copyright © 2025 Rex Zhou. All rights reserved.'
__credits__ = [__author__]
__license__ = None
__maintainer__ = __author__
__email__ = '879582094@qq.com'

from .main import app

application = app
