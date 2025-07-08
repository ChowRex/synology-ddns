#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests module

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025-07-01 10:54:29
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from logging import basicConfig, DEBUG
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from pytest import fixture

from synology_ddns import app

basicConfig(level=DEBUG, format="%(levelname)s %(name)s %(lineno)d %(message)s")
env_file = Path(__file__).parent.with_name(".env")
load_dotenv(env_file, override=True)
HOSTNAME = getenv("SYNO_DDNS_HOSTNAME")
CLOUDFLARE_USER_TOKEN = getenv("SYNO_DDNS_CLOUDFLARE_USER_TOKEN")
CLOUDFLARE_ACCOUNT_TOKEN = getenv("SYNO_DDNS_CLOUDFLARE_ACCOUNT_TOKEN")


@fixture
def client():
    """
    Create a Flask test client
    :return:
    """
    app.config['TESTING'] = True

    # pylint: disable=redefined-outer-name
    with app.test_client() as client:
        with app.app_context():
            yield client
