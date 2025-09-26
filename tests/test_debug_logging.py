#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test debug logging functionality

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025-09-25 17:21:37
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""

from synology_ddns.main import app
from synology_ddns._deco import sanitize_error_message


def test_sanitize_error_message_tokens():
    """Test sanitizing API tokens from error messages"""
    message = "Error with token: abcdefghijklmnopqrstuvwxyz1234567890"
    result = sanitize_error_message(message)
    assert "[REDACTED]" in result
    assert "abcdefghijklmnopqrstuvwxyz1234567890" not in result


def test_sanitize_error_message_passwords():
    """Test sanitizing passwords from error messages"""
    message = "URL: https://api.example.com?password=secret123&other=value"
    result = sanitize_error_message(message)
    assert "password=[REDACTED]" in result
    assert "secret123" not in result


def test_debug_logging_enabled():
    """Test debug logging when debug mode is enabled"""
    client = app.test_client()
    app.debug = True

    try:
        # This will trigger debug logging path
        data = {"api": "cloud_flare", "myip": "invalid_ip"}
        response = client.get("/", query_string=data)
        # Should return badagent due to missing parameters
        assert response.text in ["badagent", "badauth"]
    finally:
        app.debug = False
