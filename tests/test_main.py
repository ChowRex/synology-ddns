#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic test module

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025-07-01 10:54:48
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from json import loads

# pylint: disable=unused-import
from synology_ddns._response import ResponseString as Rs
from . import client


# pylint: disable=redefined-outer-name
def test_root_get(client):
    """
    Test home GET route
    :param client: TestClient object
    :return:
    """
    response = client.get("/")
    assert response.status_code == 200


def test_none_provider(client):
    """
    Test GET route for None provider
    :param client: TestClient object
    :return:
    """
    data = {"api": "", "myip": "123"}
    response = client.get("/", query_string=data)
    assert Rs.BAD_REQUEST.value == response.text


def test_version_endpoint(client):
    """
    Test version endpoint
    :param client: TestClient object
    :return:
    """
    response = client.get("/version")
    assert response.status_code == 200

    # Parse JSON response
    data = loads(response.text)

    # Verify response structure
    assert "version" in data
    assert "name" in data
    assert "description" in data

    # Verify values
    assert data["name"] == "synology-ddns"
    assert data["description"] == "Synology DSM DDNS custom provider for CloudFlare"
    assert data["version"] == "1.0.0"
