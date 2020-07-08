import logging
from typing import Dict

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def respond_404(request) -> HttpResponse:
    msg = "Error 404: File not found"
    response = render(request, msg)
    response.status_code = 404
    return response


def respond_405(request) -> HttpResponse:
    msg = "Error 405: Method not allowed"
    response = render(request, msg)
    response.status_code = 405
    return response


def respond_418(request) -> HttpResponse:
    msg = "Check the entered data"
    response = render(request, msg)
    response.status_code = 418
    return response


def respond_302(request, redirect_to, cookies_content) -> HttpResponse:
    response = HttpResponseRedirect(redirect_to)
    for name, value in cookies_content.items():
        response.set_cookie(cookies_content[name], cookies_content[value], max_age=None)
    response.status_code = 302
    return response


def send_response(
        server_inst,
        code: int,
        msg: str,
        headers: Dict = {},
        cookie_master: Dict = {}
) -> None:
    msg = msg.encode()

    server_inst.send_response(code)
    server_inst.send_header("Content-length", len(msg))
    # server_inst.send_header("Cache-Control", f"max-age={30 * 24 * 60 * 60}")

    logging.debug(f"headers = {headers}")
    for header, value in headers.items():
        server_inst.send_header(header, value)

    logging.debug(f"cookies = {cookie_master}")
    # if cookie_master is not None:
    for cookie in cookie_master.values():
        server_inst.send_header("Set-Cookie", cookie.OutputString())

    server_inst.end_headers()
    server_inst.wfile.write(msg)
