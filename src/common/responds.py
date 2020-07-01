def respond_200(server_inst, msg: str, content_type="text/plain", cookies_content="") -> None:
    send_response(server_inst, 200, msg, content_type, "", cookies_content)


def respond_404(server_inst) -> None:
    msg = "Error 404: File not found"
    send_response(server_inst, 404, msg)


def respond_405(server_inst) -> None:
    msg = "Error 405: Method not allowed"
    send_response(server_inst, 405, msg)


def respond_418(server_inst) -> None:
    msg = "Check the entered data"
    send_response(server_inst, 418, msg)


def respond_302(server_inst, redirect_to: str, cookies_content="") -> None:
    send_response(server_inst, 302, "", "text/plain", redirect_to, cookies_content)


def send_response(
        server_inst,
        code: int,
        msg: str,
        content_type="text/plain",
        redirect_to="",
        cookie_master=""
) -> None:
    msg = msg.encode()

    server_inst.send_response(code)
    server_inst.send_header("Content-type", content_type)

    if redirect_to != "":
        server_inst.send_header("Location", redirect_to)

    server_inst.send_header("Content-length", len(msg))

    print(f"cookies = {cookie_master}")
    if cookie_master != "":
        for cookie in cookie_master.values():
            server_inst.send_header("Set-Cookie", cookie.OutputString())

    # server_inst.send_header("Cache-Control", f"max-age={30 * 24 * 60 * 60}")

    server_inst.end_headers()

    server_inst.wfile.write(msg)
