#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main function

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025-07-01 10:12:19
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from pathlib import Path

from flask import Flask, request, jsonify

from . import __version__
from ._deco import handle_exceptions
from ._verify import APIProviders
from .logging_config import setup_logging

app = Flask(__name__)
setup_logging(app)


@app.route("/", methods=["GET"])
@handle_exceptions
def root():
    """
    Webhook root entrance
    If request didn't provide api and myip, return the help document.
    :return:
    """
    rules = [
        not bool(request.args.get("api", "")),
        not bool(request.args.get("myip", "")),
    ]
    if all(rules):
        docs = Path(__file__).parent / "html/index.html"
        with open(docs, "r", encoding="utf-8") as _:
            return _.read()
    provider = APIProviders.get_provider()
    return provider.update()


@app.route("/version", methods=["GET"])
def version():
    """
    Return version information
    :return: JSON response with version info
    """
    return jsonify(
        {
            "version": __version__,
            "name": "synology-ddns",
            "description": "Synology DSM DDNS custom provider for CloudFlare",
        }
    )
