#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test validation functions

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025-09-25 17:21:37
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from synology_ddns._verify import validate_ip_address, validate_hostname, sanitize_input


def test_validate_ip_address_valid():
    """Test valid IP addresses"""
    assert validate_ip_address("192.168.1.1") is True
    assert validate_ip_address("8.8.8.8") is True
    assert validate_ip_address("127.0.0.1") is True


def test_validate_ip_address_invalid():
    """Test invalid IP addresses"""
    assert validate_ip_address("256.256.256.256") is False
    assert validate_ip_address("invalid.ip") is False
    assert validate_ip_address("") is False


def test_validate_hostname_valid():
    """Test valid hostnames"""
    assert validate_hostname("example.com") is True
    assert validate_hostname("sub.example.com") is True
    assert validate_hostname("test-host.example.org") is True


def test_validate_hostname_invalid():
    """Test invalid hostnames"""
    assert validate_hostname("") is False
    assert validate_hostname("a" * 254) is False  # Too long
    assert validate_hostname("-invalid.com") is False
    assert validate_hostname("invalid-.com") is False


def test_sanitize_input_empty():
    """Test sanitize empty input"""
    assert sanitize_input("") == ""


def test_sanitize_input_control_chars():
    """Test sanitize input with control characters"""
    assert sanitize_input("test\x00\x1f") == "test"
    assert sanitize_input("test\x7f\x9f") == "test"


def test_sanitize_input_length_limit():
    """Test sanitize input length limit"""
    long_input = "a" * 300
    result = sanitize_input(long_input)
    assert len(result) == 255
