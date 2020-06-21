import socketserver
import os
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from typing import Union
from datetime import datetime
from pathlib import Path

PORT = int(os.getenv("PORT", 8000))
print(f"PORT={PORT}")


class PageNotFoundError(Exception):
    pass


def get_page(self):
    path, qs = self.path.split("?") if '?' in self.path else [self.path, ""]

    if path.endswith(".css"):
        get_cv_style(self)

    path = path.rstrip('/')
    switcher = {
        "/hello": get_page_hello,
        "/goodbye": get_page_goodbye,
        "/cv": get_page_cv,
        "/cv/job": get_page_cv_job,
        "/cv/education": get_page_cv_education,
        "/cv/skills": get_page_cv_skills,
    }

    # get a page via dict.get (usable in do_GET)
    # if switcher doesn't contain path, return SimpleHTTPRequestHandler function
    # because of it's needed to add a check for path not in switcher

    # if path not in switcher:
    #     return SimpleHTTPRequestHandler.do_GET(self)
    # default_handler = super().do_GET
    # handler = switcher.get(path, default_handler)
    # handler()

    try:
        if path in switcher:
            switcher[path](self, qs)
        else:
            # return SimpleHTTPRequestHandler.do_GET(self)
            raise PageNotFoundError
    except FileNotFoundError:
        respond_404(self)
    except PageNotFoundError:
        respond_405(self)


def get_page_hello(self, qs) -> None:
    if qs != "":
        qs = parse_qs(qs)  # return dict
    name = get_name(qs)
    year = get_year(qs)
    msg = f"""
                    Hey {name}!
                    You were born in {str(year)}.
                """
    respond_200(self, msg, "text/plain")


def get_page_goodbye(self, qs) -> None:
    msg = f"""
                    {say_bye(datetime.today().hour)}
                    Time: {datetime.today()}
                 """
    respond_200(self, msg, "text/plain")


def get_name(qs) -> str:
        return qs["name"][0] if "name" in qs else "Dude"


def get_year(qs) -> Union[int, str]:
    today = datetime.today().year
    return today - int(qs["age"][0]) if "age" in qs else "-"


def say_bye(hour) -> str:
    if hour < 0:
        return "Invalid value."
    elif hour < 6 or hour == 23:
        return "Goodnight!"
    elif hour < 12:
        return "Good Morning!"
    elif hour < 18:
        return "Have a nice day!"
    elif hour < 23:
        return "Good Evening!"
    else:
        return "Invalid value."


def get_cv_style(self) -> None:
    msg = get_file_contents("pages/cv_style.css")
    respond_200(self, msg, "text/css")


def get_page_cv(self, _qs) -> None:
    msg = get_file_contents("pages/cv_common.html")
    respond_200(self, msg, "text/html")


def get_page_cv_education(self, _qs) -> None:
    msg = get_file_contents("pages/cv_education.html")
    respond_200(self, msg, "text/html")


def get_page_cv_job(self, _qs) -> None:
    msg = get_file_contents("pages/cv_job.html")
    respond_200(self, msg, "text/html")


def get_page_cv_skills(self, _qs) -> None:
    msg = get_file_contents("pages/cv_skills.html")
    respond_200(self, msg, "text/html")


def get_file_contents(file_path) -> str:
    full_file_path = Path(__file__).parent.parent.resolve() / file_path  # full path to dir where file is located
    if not full_file_path.is_file():
        raise FileNotFoundError
    with full_file_path.open("r", encoding="utf-8") as file_src:
        content = file_src.read()
    return content


def respond_200(self, msg: str, content_type="text/plain") -> None:
    msg = msg.encode()

    self.send_response(200)
    self.send_header("Content-type", content_type)
    self.send_header("Content-length", len(msg))
    self.end_headers()

    self.wfile.write(msg)


def respond_404(self) -> None:
    msg = "Error 404: File not found"
    msg = msg.encode()

    self.send_response(404)
    self.send_header("Content-type", "text/plain")
    self.send_header("Content-length", len(msg))
    self.end_headers()

    self.wfile.write(msg)


def respond_405(self) -> None:
    msg = "Error 405: Page not found"
    msg = msg.encode()

    self.send_response(405)
    self.send_header("Content-type", "text/plain")
    self.send_header("Content-length", len(msg))
    self.end_headers()

    self.wfile.write(msg)


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            get_page(self)
        else:
            return SimpleHTTPRequestHandler.do_GET(self)


if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        # httpd = socketserver.TCPServer(("", PORT), MyHandler)
        print("it works")
        httpd.serve_forever()