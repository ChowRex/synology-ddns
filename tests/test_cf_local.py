#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for CloudFlare local

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025-07-01 10:55:14
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from os import environ
from traceback import format_exc

# pylint: disable=protected-access,unused-import
from synology_ddns._response import ResponseString as Rs
from synology_ddns.api import CloudFlareDDNS
from . import client, HOSTNAME, env_file


# pylint: disable=redefined-outer-name
def test_wrong_provider(client):
    """
    Test GET route for wrong provider
    :param client: TestClient object
    :return:
    """
    data = {"api": "wrong_provider", "myip": "123"}
    response = client.get("/", query_string=data)
    assert Rs.BAD_REQUEST.value == response.text


# pylint: disable=redefined-outer-name
def test_lack_argument(client):
    """
    Test GET route for lack argument
    :param client: TestClient object
    :return:
    """
    data = {"api": "cloud_flare"}
    response = client.get("/", query_string=data)
    assert Rs.BAD_REQUEST.value == response.text


# pylint: disable=redefined-outer-name
def test_lack_parameter(client):
    """
    Test GET route for lack parameter
    :param client: TestClient object
    :return:
    """
    if env_file.exists():
        new_name = ".env.rename"
        try:
            env_file.rename(new_name)
            environ.pop("SYNO_DDNS_HOSTNAME")
            data = {"api": "cloud_flare", "myip": "123"}
            response = client.get("/", query_string=data)
            assert Rs.BAD_REQUEST.value == response.text
        except AssertionError as error:  # pragma:no cover
            print(error)
            print(format_exc())
        finally:
            env_file.with_name(new_name).rename(".env")
    else:
        hostname = environ.pop("SYNO_DDNS_HOSTNAME")
        try:
            data = {"api": "cloud_flare", "myip": "123"}
            response = client.get("/", query_string=data)
            assert Rs.BAD_REQUEST.value == response.text
        except AssertionError as error:  # pragma:no cover
            print(error)
            print(format_exc())
        finally:
            environ["SYNO_DDNS_HOSTNAME"] = hostname


# pylint: disable=redefined-outer-name
def test_wrong_fqdn(client):
    """
    Test GET route for wrong FQDN
    :param client: TestClient object
    :return:
    """
    data = {"api": "cloud_flare", "hostname": "aaaa", "myip": "123"}
    response = client.get("/", query_string=data)
    assert Rs.NOT_FQDN.value == response.text


# pylint: disable=redefined-outer-name
def test_not_changed(client):
    """
    Test GET route for not changed
    :param client: TestClient object
    :return:
    """
    CloudFlareDDNS._LATEST_RECORDS[HOSTNAME] = "000"
    data = {"api": "cloud_flare", "myip": "000"}
    response = client.get("/", query_string=data)
    assert Rs.NO_CHANGE.value == response.text


# pylint: disable=redefined-outer-name
def test_not_resolve(client):
    """
    Test GET route for not resolved
    :param client: TestClient object
    :return:
    """
    endpoint = CloudFlareDDNS._END_POINT
    try:
        CloudFlareDDNS._END_POINT = "https://a.xxx.domain"
        data = {"api": "cloud_flare", "myip": "123"}
        response = client.get("/", query_string=data)
        assert Rs.BAD_RESOLVE.value == response.text
    except AssertionError:  # pragma: no cover
        ...
    finally:
        CloudFlareDDNS._END_POINT = endpoint
