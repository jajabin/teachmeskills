def respond_200(self, msg: str, content_type="text/plain", cookies_content="") -> None:
    send_response(self, 200, msg, content_type, "", cookies_content)


def respond_404(self) -> None:
    msg = "Error 404: File not found"
    send_response(self, 404, msg, "text/plain")


def respond_405(self) -> None:
    msg = "Error 405: Method not allowed"
    send_response(self, 405, msg, "text/plain")


def respond_418(self) -> None:
    msg = "Check the entered data"
    send_response(self, 418, msg, "text/plain")


def respond_302(self, redirect_to: str, cookies_content="") -> None:
    send_response(self, 302, "", "text/plain", redirect_to, cookies_content)


def send_response(self, code: int, msg: str, content_type: str, redirect_to="", cookie_master="") -> None:
    msg = msg.encode()

    self.send_response(code)
    self.send_header("Content-type", content_type)

    if redirect_to != "":
        self.send_header("Location", redirect_to)

    self.send_header("Content-length", len(msg))

    print(f"cookies = {cookie_master}")
    if cookie_master != "":
        for item in cookie_master.values():
            self.send_header("Set-Cookie", item.OutputString())

    # self.send_header("Cache-Control", f"max-age={30 * 24 * 60 * 60}")

    self.end_headers()

    self.wfile.write(msg)