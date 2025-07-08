#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main function

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025-07-01 10:12:19
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from pathlib import Path

from flask import Flask, request

from ._deco import handle_exceptions
from ._verify import APIProviders

app = Flask(__name__)


@app.route('/', methods=["GET"])
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
