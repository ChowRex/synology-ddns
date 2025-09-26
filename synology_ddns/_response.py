#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Standard response module

- Author: Rex Zhou <879582094@qq.com>
- Created Time: 2025/7/1 10:36
- Copyright: Copyright © 2025 Rex Zhou. All rights reserved.
"""

from enum import Enum


# pylint: disable=line-too-long
class ResponseString(Enum):
    """
    Standard response string.

    From `/etc.defaults/ddns_provider.conf`

    Input:
        1. DynDNS style request:
            modulepath = DynDNS
            queryurl = [Update URL]?[Query Parameters]

        2. Self-defined module:
            modulepath = /sbin/xxxddns
            queryurl = DDNS_Provider_Name

            Our service will assign parameters in the following order when calling module:
                ($1=username, $2=password, $3=hostname, $4=ip)

    Output:
        When you write your own module, you can use the following words to tell user what happen by print it.
        You can use your own message, but there is no multiple-language support.

            good -  Update successfully.
            nochg - Update successfully but the IP address have not changed.
            nohost - The hostname specified does not exist in this user account.
            abuse - The hostname specified is blocked for update abuse.
            notfqdn - The hostname specified is not a fully-qualified domain name.
            badauth - Authenticate failed.
            911 - There is a problem or scheduled maintenance on provider side
            badagent - The user agent sent bad request(like HTTP method/parameters is not permitted)
            badresolv - Failed to connect to  because failed to resolve provider address.
            badconn - Failed to connect to provider because connection timeout.

    """

    OK = "good"
    NO_CHANGE = "nochg"
    NO_HOST = "nohost"
    ABUSE = "abuse"
    NOT_FQDN = "notfqdn"
    BAD_AUTH = "badauth"
    API_ERROR = "911"
    BAD_REQUEST = "badagent"
    BAD_RESOLVE = "badresolv"
    BAD_CONNECTION = "badconn"
