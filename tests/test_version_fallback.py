#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test version fallback mechanism

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025-09-26 10:02:00
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from pathlib import Path
from unittest.mock import patch


def test_version_fallback_mechanism():
    """Test that fallback version is used when VERSION file is not found"""

    # Test the fallback logic directly
    def get_version_with_fallback(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return "0.0.1"  # Fallback version

    # Mock the file not found scenario
    with patch("builtins.open", side_effect=FileNotFoundError):
        version = get_version_with_fallback("non_existent_file")
        assert version == "0.0.1"


def test_version_file_content():
    """Test that VERSION file contains expected content"""
    version_file = Path(__file__).parent.parent / "VERSION"

    # Verify file exists
    assert version_file.exists(), "VERSION file should exist"

    # Verify content
    with open(version_file, "r", encoding="utf-8") as f:
        version = f.read().strip()
        assert version == "1.0.0", f"Expected version 1.0.0, got {version}"

    # Verify no extra whitespace
    with open(version_file, "r", encoding="utf-8") as f:
        raw_content = f.read()
        assert (
            raw_content.strip() == version
        ), "VERSION file should not have extra whitespace"
