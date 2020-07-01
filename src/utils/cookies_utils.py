from datetime import datetime, timedelta
from http import cookies
from typing import Dict

import src.common.instances as instance


def get_cookies(self) -> Dict[str, str]:
    cookies_content = self.headers.get('Cookie')
    if cookies_content is None:  # if not cookies_content:
        return {}
    cookies_content = cookies_content.replace(" ", "")
    cookies_content = dict(cookie.split("=") for cookie in cookies_content.split(";"))
    return cookies_content


def set_cookies(self, cookies_content: dict):
    cookie_master = cookies.SimpleCookie(self.headers.get('Cookie'))
    expired_date = datetime.now() + timedelta(days=instance.COOKIE_TERM)
    for name, value in cookies_content.items():
        cookie_master[name] = value
        cookie_master[name]["expires"] = expired_date.strftime("%a, %d-%b-%Y %H:%M:%S PST")
        cookie_master[name]["path"] = "/"
    return cookie_master
