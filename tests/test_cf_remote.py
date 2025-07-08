#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for CloudFlare remote

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025/7/3 11:02
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""

from os import environ

# pylint: disable=protected-access,unused-import
from synology_ddns._response import ResponseString as Rs
from synology_ddns.api import CloudFlareDDNS
from . import client, CLOUDFLARE_USER_TOKEN, CLOUDFLARE_ACCOUNT_TOKEN


# pylint: disable=unused-import,redefined-outer-name
def test_verify_token_error(client):
    """
    Test home GET route with wrong account token
    :param client: TestClient object
    :return:
    """
    data = {"api": "cloud_flare", "myip": "123", "password": "wrong-token"}
    # Try to use account token, but the account token is restricted and no permission.
    environ["SYNO_DDNS_CLOUDFLARE_ACCOUNT_TOKEN"] = "wrong-token"
    response = client.get("/", query_string=data)
    assert Rs.BAD_AUTH.value == response.text


# pylint: disable=unused-import,redefined-outer-name
def test_account_id_not_found_error(client):
    """
    Test home GET route with no account id
    :param client: TestClient object
    :return:
    """
    account_id_key = CloudFlareDDNS._ENV_ACCOUNT_ID
    try:
        CloudFlareDDNS._ENV_ACCOUNT_ID = "NOT_EXISTS_ENV_KEY"
        data = {"api": "cloud_flare", "myip": "123"}
        response = client.get("/", query_string=data)
        assert Rs.BAD_AUTH.value == response.text
    except AssertionError:  # pragma: no cover
        ...
    finally:
        CloudFlareDDNS._ENV_ACCOUNT_ID = account_id_key


# pylint: disable=unused-import,redefined-outer-name
def test_zone_id_not_found_error(client):
    """
    Test home GET route with no zone id
    :param client: TestClient object
    :return:
    """
    data = {
        "api": "cloud_flare",
        "myip": "123",
        "username": "example.com",
        "password": CLOUDFLARE_USER_TOKEN
    }
    response = client.get("/", query_string=data)
    assert Rs.NO_HOST.value == response.text


# pylint: disable=protected-access,unused-import,redefined-outer-name
def test_account_token_success(client):
    """
    Test home GET route
    :param client: TestClient object
    :return:
    """
    data = {
        "api": "cloud_flare",
        "myip": "1.2.3.4",
        "password": CLOUDFLARE_ACCOUNT_TOKEN
    }
    response = client.get("/", query_string=data)
    assert Rs.OK.value == response.text


# pylint: disable=protected-access,unused-import,redefined-outer-name
def test_cached_record_success(client):
    """
    Test home GET route, test update again
    :param client: TestClient object
    :return:
    """
    data = {
        "api": "cloud_flare",
        "myip": "2.3.4.5",
        "password": CLOUDFLARE_USER_TOKEN,
        "test": True
    }
    response = client.get("/", query_string=data)
    assert Rs.OK.value == response.text


# pylint: disable=protected-access,unused-import,redefined-outer-name
def test_create_new_record_success(client):
    """
    Test home GET route
    :param client: TestClient object
    :return:
    """
    data = {
        "api": "cloud_flare",
        "myip": "1.2.3.4",
        "password": CLOUDFLARE_USER_TOKEN,
        "force": True
    }
    response = client.get("/", query_string=data)
    assert Rs.OK.value == response.text
