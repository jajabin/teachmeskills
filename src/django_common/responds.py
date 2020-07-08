import logging
from typing import Dict

from django.http import HttpResponse
from django.shortcuts import render


def respond_200(server_inst, msg: str, content_type="text/plain", cookies_content={}) -> None:
    headers = {
        "Content-type": content_type
    }
    send_response(server_inst, 200, msg, headers, cookies_content)


def respond_404(request) -> HttpResponse:
    msg = "Error 404: File not found"
    response = render(request, msg)
    response.status_code = 404
    return response


def respond_405(request) -> None:
    msg = "Error 405: Method not allowed"
    response = render(request, msg)
    response.status_code = 405
    return response


def respond_418(request) -> None:
    msg = "Check the entered data"
    response = render(request, msg)
    response.status_code = 418
    return response


def respond_302(server_inst, redirect_to: str, cookies_content={}) -> None:
    headers = {
        "Content-type": "text/plain",
        "Location": redirect_to
    }
    send_response(server_inst, 302, "", headers, cookies_content)


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
