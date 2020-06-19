import socketserver
import os
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
import codecs
from datetime import datetime

PORT = int(os.getenv("PORT", 8000))
print(f"PORT={PORT}")


def get_page(self):
    path, qs = self.path.split("?") if '?' in self.path else [self.path, ""]

    if path.endswith(".css"):
        return get_cv_style()

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

    return switcher[path](qs) if path in switcher else SimpleHTTPRequestHandler.do_GET(self)


def get_page_hello(qs):
    if qs != "":
        qs = parse_qs(qs)  # return dict
    name = get_name(qs)
    year = get_year(qs)
    return f"""
                    <p>Hey {name}!</p>
                    <p>You were born in {year}.</p>
                """


def get_page_goodbye(qs):
    return f"""
                    <p>{say_bye(datetime.today().hour)}</p>
                    <p>Time: {datetime.today()}</p>
                 """


def get_name(qs):
        return qs["name"][0] if "name" in qs else "Dude"


def get_year(qs):
    today = datetime.today().year
    return str(today - int(qs["age"][0])) if "age" in qs else "-"


def say_bye(hour):
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


def get_cv_style():
    return codecs.open("pages/cv_style.css", "r", "utf-8").read()


def get_page_cv(qs):
    return codecs.open("pages/cv_common.html", "r", "utf-8").read()


def get_page_cv_education(qs):
    return codecs.open("pages/cv_education.html", "r", 'utf-8').read()


def get_page_cv_job(qs):
    return codecs.open("pages/cv_job.html", "r", 'utf-8').read()


def get_page_cv_skills(qs):
    return codecs.open("pages/cv_skills.html", "r", 'utf-8').read()


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            msg = get_page(self)
            msg = msg.encode()

            self.send_response(200)
            if self.path.endswith(".css"):
                self.send_header("Content-type", "text/css")
            else:
                self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(msg))
            self.end_headers()

            self.wfile.write(msg)

        else:
            return SimpleHTTPRequestHandler.do_GET(self)


if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        # httpd = socketserver.TCPServer(("", PORT), MyHandler)
        print("it works")
        httpd.serve_forever()