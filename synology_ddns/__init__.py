#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synology DSM DDNS customer provider.

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025/6/30 17:05
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""

from pathlib import Path

# Read version from VERSION file
_version_file = Path(__file__).parent.parent / "VERSION"
try:
    with open(_version_file, "r", encoding="utf-8") as f:
        __version__ = f.read().strip()
except FileNotFoundError:  # pragma: no cover
    __version__ = "1.0.0"  # Fallback version

__author__ = "Rex Zhou"
__copyright__ = "Copyright © 2025 Rex Zhou. All rights reserved."
__credits__ = [__author__]
__license__ = "MIT"
__maintainer__ = __author__
__email__ = "879582094@qq.com"
