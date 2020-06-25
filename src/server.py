import socketserver
import os
import json
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from typing import Union
from typing import Dict
from datetime import datetime
from pathlib import Path

PORT = int(os.getenv("PORT", 8000))
print(f"PORT={PORT}")


class PageNotFoundError(Exception): #what's Exception and RuntimeError ???
    pass


class MethodNotAllowed(Exception):
    pass


class UnknownPath(Exception):
    pass


def do(self, method: str) -> None:
    path, qs = self.path.split("?") if '?' in self.path else [self.path, ""]

    if path == "/":
        return SimpleHTTPRequestHandler.do_GET(self)

    if path.endswith(".css"):
        get_cv_style(self, method)
        return

    path = path.rstrip('/')
    switcher = {
        "/hello": get_page_hello,
        "/goodbye": get_page_goodbye,
        "/cv": get_page_cv,
        "/cv/job": get_page_cv_job,
        "/cv/education": get_page_cv_education,
        "/cv/skills": get_page_cv_skills,
        "/statistics": get_page_statistics,
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
            switcher[path](self, method, qs)
        else:
            # return SimpleHTTPRequestHandler.do_GET(self)
            print(path)
            raise PageNotFoundError
    except (FileNotFoundError, PageNotFoundError):
        respond_404(self)
    except MethodNotAllowed:
        respond_405(self)


def get_page_hello(self, method: str, qs: str) -> None:
    switcher = {
        "GET": show_page_hello,
        "POST": save_user_data,
    }
    if method in switcher:
        switcher[method](self)
    else:
        raise MethodNotAllowed

    # if qs != "":
    #     qs = parse_qs(qs)  # return dict
    # #name = get_name(qs)
    # #year = get_year(qs)
    # msg = get_file_contents("pages/hello.html").format(name='DJANGO', year=76) #format ???
    # respond_200(self, msg, "text/html")


def show_page_hello(self):
    #increment_page_visit(self, "/hello")
    user_data = read_data(self, "sessions.json")
    name = user_data["name"] if "name" in user_data else "Dude"
    today = datetime.today().year
    year = today - int(user_data["age"]) if "age" in user_data else "-"
    msg = get_file_contents("pages/hello.html").format(name=name, year=year) #format ???
    respond_200(self, msg, "text/html")


def save_user_data(self):
    user_data = get_user_data(self)
    update_user_sessions(self, user_data)
    respond_302(self, "/hello")


# def increment_page_visit(self, endpoint: str) -> None:
#     statistics_content = read_data(self, "visit_counters.json")
#     today = datetime.today().date()
#
#     if endpoint in statistics_content:
#         if today in statistics_content[endpoint]:
#             print(statistics_content[endpoint][today])
#             #statistics_content[endpoint][today] += 1
#         else:
#             statistics_content[endpoint][today] =
#     print(statistics_content[endpoint][today])


def get_user_data(self) -> Dict[str, str]:
    content_length = int(self.headers["Content-Length"])
    data = self.rfile.read(content_length)
    payload = data.decode()
    qs = parse_qs(payload)
    user_data = {}
    for key, values in qs.items():
        if not values:
            continue
        user_data[key] = values[0]

    return user_data


def update_user_sessions(self, user_data):
    sessions = read_data(self, "sessions.json")
    sessions.update(user_data)  # what does update ???
    write_data(self, "sessions.json", sessions)


def read_data(self, path: str) -> Dict:
    file_path = Path(__file__).parent.parent.resolve() / path
    try:
        with file_path.open("r", encoding="utf-8") as usf:
            return json.load(usf)   #what does load?
    except (json.JSONDecodeError, FileNotFoundError):
        print("-> load_user_sessions: exception")
        return {}   #return error!!!


def write_data(self, path: str, sessions: Dict) -> None:
    file_path = Path(__file__).parent.parent.resolve() / path
    with file_path.open("w") as usf:
        json.dump(sessions, usf)


def get_page_goodbye(self, _method, _qs) -> None:
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


def get_cv_style(self, _method) -> None:
    msg = get_file_contents("pages/cv_style.css")
    respond_200(self, msg, "text/css")


def get_page_cv(self, _method, _qs) -> None:
    resume_content = read_data(self, "contents/cv_resume.json")
    msg = get_file_contents("pages/cv_common.html").format(**resume_content)
    respond_200(self, msg, "text/html")


def get_page_cv_education(self, _method, _qs) -> None:
    resume_content = read_data(self, "contents/cv_resume.json")
    msg = get_file_contents("pages/cv_education.html").format(**resume_content)
    respond_200(self, msg, "text/html")


def get_page_cv_job(self, _method, _qs) -> None:
    resume_content = read_data(self, "contents/cv_resume.json")
    msg = get_file_contents("pages/cv_job.html").format(**resume_content)
    respond_200(self, msg, "text/html")


def get_page_cv_skills(self, _method, _qs) -> None:
    resume_content = read_data(self, "contents/cv_resume.json")
    msg = get_file_contents("pages/cv_skills.html").format(**resume_content)
    respond_200(self, msg, "text/html")


def get_page_statistics(self, _method, _qs) -> None:
    statistics_content = read_data(self, "visit_counters.json")
    msg = get_file_contents("pages/statistics.html")
    respond_200(self, msg, "text/html")


def get_file_contents(file_path) -> str:
    full_file_path = Path(__file__).parent.parent.resolve() / file_path  # full path to dir where file is located
    if not full_file_path.is_file():
        raise FileNotFoundError
    with full_file_path.open("r", encoding="utf-8") as file_src:
        content = file_src.read()
    return content


def respond_200(self, msg: str, content_type="text/plain") -> None:
    send_response(self, 200, msg, content_type)


def respond_404(self) -> None:
    msg = "Error 404: File not found"
    send_response(self, 404, msg, "text/plain")


def respond_405(self) -> None:
    msg = "Error 405: Method not allowed"
    send_response(self, 405, msg, "text/plain")


def respond_302(self, redirect_to: str) -> None:
    send_response(self, 302, "", "text/plain", redirect_to)


def send_response(self, code: int, msg: str, content_type: str, redirect_to="") -> None:
    msg = msg.encode()

    self.send_response(code)
    self.send_header("Content-type", content_type)
    if redirect_to != "":
        self.send_header("Location", redirect_to)
    self.send_header("Content-length", len(msg))
    self.send_header("Content-length", len(msg))
    self.end_headers()

    self.wfile.write(msg)


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # if self.path != "/":
        #     get_page(self)
        # else:
        #     return SimpleHTTPRequestHandler.do_GET(self)
        try:
            do(self, "GET")
        except UnknownPath:
            SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        try:
            do(self, "POST")
        except UnknownPath:
            SimpleHTTPRequestHandler.do_GET(self)


if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        # httpd = socketserver.TCPServer(("", PORT), MyHandler)
        print("it works")
        httpd.serve_forever()