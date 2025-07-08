#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parameters module

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025/7/2 14:16
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""
from pathlib import Path
from os import getenv
from typing import Final

from flask import request, current_app

from dotenv import load_dotenv


class Parameters:
    """Parameters class"""

    ENV_PREFIX: Final[str] = "SYNO_DDNS"

    def __init__(self) -> None:
        self._file = Path(__file__).parent.with_name(".env")
        self._load_dotenv()

    def _load_dotenv(self) -> None:
        """
        Load dotenv file
        :return: None
        """
        try:
            load_dotenv(self._file, override=True)
        except FileNotFoundError:  # pragma: no cover
            current_app.logger.warning(".env file not found")

    def get(self, key: str) -> str:
        """
        Get value from request and environment variables
        :param key: The name of variable
        :return: Value
        """
        key = key.strip().lower()
        result = ""
        for argument, value in request.args.items():
            if key == argument.lower():
                result = value
        if not result:
            key = f"{self.ENV_PREFIX}_{key.upper()}"
            result = getenv(key)
            if not result:
                self._load_dotenv()
                result = getenv(key)
        return result

    @property
    def hostname(self) -> str:
        """
        Return hostname
        :return: Hostname
        """
        return self.get("hostname")

    @property
    def myip(self) -> str:
        """
        Return myip
        :return: My IP address
        """
        return request.args.get("myip", "")

    @property
    def username(self) -> str:
        """
        Return username
        :return: The username
        """
        return self.get("username")

    @property
    def password(self) -> str:
        """
        Return password
        :return: The password
        """
        return self.get("password")


params = Parameters()
