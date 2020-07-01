import logging
import os
import socketserver
from http.server import SimpleHTTPRequestHandler

import src.common.errors as errors
import src.common.responds as responds
import src.pages.cv_page as cv
from src.pages.goodbye_page import get_page_goodbye
from src.pages.hello_page import get_page_hello
from src.pages.statistics_page import get_page_statistics
from src.styles.css_style import get_cv_style

PORT = int(os.getenv("PORT", 8000))
print(f"PORT={PORT}")


def do(self, method: str) -> None:
    endpoint, qs = self.path.split("?") if '?' in self.path else [self.path, ""]

    if endpoint == "/":
        return SimpleHTTPRequestHandler.do_GET(self)

    if endpoint.endswith(".css"):
        get_cv_style(self, method)
        return

    endpoint = endpoint.rstrip('/')
    switcher = {
        "/hello": get_page_hello,
        "/hello/save": get_page_hello,
        "/hello/set_night_mode": get_page_hello,
        "/goodbye": get_page_goodbye,
        "/goodbye/set_night_mode": get_page_goodbye,
        "/cv": cv.get_page_cv,
        "/cv/set_night_mode": cv.get_page_cv,
        "/cv/job": cv.get_page_cv_job,
        "/cv/job/set_night_mode": cv.get_page_cv_job,
        "/cv/education": cv.get_page_cv_education,
        "/cv/education/set_night_mode": cv.get_page_cv_education,
        "/cv/skills": cv.get_page_cv_skills,
        "/cv/skills/set_night_mode": cv.get_page_cv_skills,
        "/cv/projects": cv.get_page_cv_projects,
        "/cv/projects/set_night_mode": cv.get_page_cv_projects,
        "/statistics": get_page_statistics,
        "/statistics/set_night_mode": get_page_statistics,
        "/cv/projects/editing": cv.get_page_projects_editing,
        "/cv/projects/editing/add": cv.get_page_projects_editing,
        "/cv/projects/editing/edit": cv.get_page_projects_editing,
        "/cv/projects/editing/delete": cv.get_page_projects_editing,
        "/cv/projects/editing/set_night_mode": cv.get_page_projects_editing,
    }

    # get a page via dict.get (usable in do_GET)
    # if switcher doesn't contain endpoint, return SimpleHTTPRequestHandler function
    # because of it's needed to add a check for endpoint not in switcher

    # if endpoint not in switcher:
    #     return SimpleHTTPRequestHandler.do_GET(self)
    # default_handler = super().do_GET
    # handler = switcher.get(endpoint, default_handler)
    # handler()

    try:
        if endpoint in switcher:
            switcher[endpoint](self, method, endpoint, qs)
        else:
            # return SimpleHTTPRequestHandler.do_GET(self)
            raise errors.PageNotFoundError
    except (FileNotFoundError, errors.PageNotFoundError):
        responds.respond_404(self)
    except errors.MethodNotAllowed:
        responds.respond_405(self)


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # if self.path != "/":
        #     get_page(self)
        # else:
        #     return SimpleHTTPRequestHandler.do_GET(self)
        try:
            do(self, "GET")
        except errors.UnknownPath:
            SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        try:
            do(self, "POST")
        except errors.UnknownPath:
            SimpleHTTPRequestHandler.do_POST(self)


if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        # httpd = socketserver.TCPServer(("", PORT), MyHandler)
        logging.info('it works')
        httpd.serve_forever()
