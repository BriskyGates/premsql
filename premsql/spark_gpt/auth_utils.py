# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Dragon
@Version        :  WIN10, Python3.7.9
------------------------------------
@IDE            ： PyCharm
@Description    :  
@CreateTime     :  12/14/2024 10:53 AM
------------------------------------
"""
from datetime import datetime
import hmac
import base64
from urllib.parse import urlparse, quote
import hashlib


class AuthUtils:
    @staticmethod
    def assemble_request_url(request_url: str, api_key: str, api_secret: str) -> str:
        # Convert WebSocket URL to HTTP URL for parsing
        # http_request_url = request_url.replace("ws://", "http://").replace("wss://", "https://")
        http_request_url=request_url
        url = urlparse(http_request_url)

        # Generate UTC timestamp
        date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        host = url.hostname

        # Create string to sign
        string_to_sign = (
            f"host: {host}\n"
            f"date: {date}\n"
            f"GET {url.path} HTTP/1.1"
        )
        print(string_to_sign)

        # Calculate HMAC-SHA256
        signature = hmac.new(
            api_secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()
        sha = base64.b64encode(signature).decode('utf-8')

        # Create authorization string
        authorization = (
            f'hmac api_key="{api_key}", algorithm="hmac-sha256", '
            f'headers="host date request-line", signature="{sha}"'
        )
        auth_base = base64.b64encode(authorization.encode('utf-8')).decode('utf-8')

        # Construct final URL
        return f"{request_url}?authorization={quote(auth_base)}&host={quote(host)}&date={quote(date)}"
