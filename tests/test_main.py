#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic test module

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025-07-01 10:54:48
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""

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
    response = client.get('/')
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
