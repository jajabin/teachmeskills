from typing import Dict
from http import cookies
from datetime import datetime, timedelta


def get_cookies(self) -> Dict[str, str]:
    cookies_content = self.headers.get('Cookie')
    if cookies_content == None:
        return {}
    cookies_content = cookies_content.replace(" ", "")
    cookies_content = dict(cookie.split("=") for cookie in cookies_content.split(";"))
    return cookies_content


def set_cookies(self, cookies_content: dict):
    cookie_master = cookies.SimpleCookie(self.headers.get('Cookie'))
    expired_date = datetime.now() + timedelta(days=30)
    for key, value in cookies_content.items():
        cookie_master[key] = value
        cookie_master[key]["expires"] = expired_date.strftime("%a, %d-%b-%Y %H:%M:%S PST")
        cookie_master[key]["path"] = "/"
    return cookie_master