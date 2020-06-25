import socketserver
import os
import json
import cgi
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from typing import Union
from typing import Dict
from datetime import datetime, timedelta
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
    endpoint, qs = self.path.split("?") if '?' in self.path else [self.path, ""]

    if endpoint == "/":
        return SimpleHTTPRequestHandler.do_GET(self)

    if endpoint.endswith(".css"):
        get_cv_style(self, method)
        return

    endpoint = endpoint.rstrip('/')
    switcher = {
        "/hello": get_page_hello,
        "/goodbye": get_page_goodbye,
        "/cv": get_page_cv,
        "/cv/job": get_page_cv_job,
        "/cv/education": get_page_cv_education,
        "/cv/skills": get_page_cv_skills,
        "/cv/projects": get_page_cv_projects,
        "/statistics": get_page_statistics,
        "/cv/projects/editing": get_page_editing,
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
            print(endpoint)
            raise PageNotFoundError
    except (FileNotFoundError, PageNotFoundError):
        respond_404(self)
    except MethodNotAllowed:
        respond_405(self)


def get_page_hello(self, method: str, endpoint: str, qs: str) -> None:
    switcher = {
        "GET": show_page_hello,
        "POST": save_user_data,
    }
    if method in switcher:
        switcher[method](self, endpoint)
    else:
        raise MethodNotAllowed

    # if qs != "":
    #     qs = parse_qs(qs)  # return dict
    # #name = get_name(qs)
    # #year = get_year(qs)
    # msg = get_file_contents("pages/hello.html").format(name='DJANGO', year=76) #format ???
    # respond_200(self, msg, "text/html")


def show_page_hello(self, endpoint: str):
    increment_page_visit(self, endpoint)
    user_data = read_json_file(self, "sessions.json")
    name = user_data["name"] if "name" in user_data else "Dude"
    today = datetime.today().year
    year = today - int(user_data["age"]) if "age" in user_data else "-"
    msg = get_file_contents("pages/hello.html").format(name=name, year=year) #format ???
    respond_200(self, msg, "text/html")


def save_user_data(self, _endpoint):
    user_data = get_user_data(self)
    update_user_sessions(self, user_data)
    respond_302(self, "/hello")


def increment_page_visit(self, endpoint: str) -> None:
    today = str(datetime.today().date())
    statistics_content = read_json_file(self, "visit_counters.json")

    if endpoint not in statistics_content:
        statistics_content[endpoint] = {}
    if today not in statistics_content[endpoint]:
        statistics_content[endpoint][today] = 0

    statistics_content[endpoint][today] += 1
    write_json_file(self, "visit_counters.json", statistics_content)


def get_user_data(self) -> Dict[str, str]:
    content_length = int(self.headers["Content-Length"])
    data = self.rfile.read(content_length)
    print(f"data = {data}")
    payload = data.decode()
    print(payload)
    qs = parse_qs(payload)
    user_data = {}
    for key, values in qs.items():
        if not values:
            continue
        user_data[key] = values[0]

    return user_data


def update_user_sessions(self, user_data):
    sessions = read_json_file(self, "sessions.json")
    sessions.update(user_data)  # what does update ???
    write_json_file(self, "sessions.json", sessions)


def read_json_file(self, path: str) -> Dict:
    file_path = Path(__file__).parent.parent.resolve() / path
    try:
        with file_path.open("r", encoding="utf-8") as usf:
            return json.load(usf)   #what does load?
    except (json.JSONDecodeError, FileNotFoundError):
        print("-> load_user_sessions: exception")
        return {}   #return error!!!


def write_json_file(self, path: str, data: Dict) -> None:
    file_path = Path(__file__).parent.parent.resolve() / path
    with file_path.open("w") as usf:
        json.dump(data, usf)


def get_page_goodbye(self, _method, endpoint: str, _qs) -> None:
    increment_page_visit(self, endpoint)
    today = datetime.today()
    phrase = say_bye(today.hour)
    msg = get_file_contents("pages/goodbye.html").format(date=today, phrase=phrase)  # format ???
    respond_200(self, msg, "text/html")


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


def get_colors(content):
    return content["background_color"], content["text_color"]


def get_page_cv(self, method: str, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "contents/cv_resume.json", "pages/cv.html")
    else:
        raise MethodNotAllowed


def get_page_cv_education(self, method: str, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "contents/cv_resume.json", "pages/cv_education.html")
    else:
        raise MethodNotAllowed


def get_page_cv_job(self, method, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "contents/cv_resume.json", "pages/cv_job.html")
    else:
        raise MethodNotAllowed


def get_page_cv_skills(self, method, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "contents/cv_resume.json", "pages/cv_skills.html")
    else:
        raise MethodNotAllowed


def get_page_cv_projects(self, method, endpoint, _qs) -> None:
    if method == "GET":
        increment_page_visit(self, endpoint)
        resume_content = read_json_file(self, "contents/cv_resume.json")

        colors = read_json_file(self, "night_mode.json")
        background_color, text_color = get_colors(colors)

        msg = get_file_contents("pages/header.html").format(bcolor=background_color, tcolor=text_color, **resume_content)
        msg += get_file_contents("pages/cv_projects.html").format(**resume_content["projects"])
        msg += get_file_contents("pages/footer.html")

        respond_200(self, msg, "text/html")

    if method == "POST":
        save_page_cv(self, endpoint, "contents/cv_resume.json", "pages/cv_projects.html")


def show_page_cv(self, endpoint: str, file_content: str, file_html: str):
    increment_page_visit(self, endpoint)
    resume_content = read_json_file(self, file_content)

    colors = read_json_file(self, "night_mode.json")
    background_color, text_color = get_colors(colors)

    msg = get_file_contents("pages/header.html").format(bcolor=background_color, tcolor=text_color, **resume_content)
    msg += get_file_contents(file_html).format(**resume_content)
    msg += get_file_contents("pages/footer.html")

    respond_200(self, msg, "text/html")


def save_page_cv(self, endpoint: str, _file_content, _file_html):
    colors = read_json_file(self, "night_mode.json")
    text_color, background_color = get_colors(colors)
    colors["background_color"] = background_color
    colors["text_color"] = text_color
    write_json_file(self, "night_mode.json", colors)
    respond_302(self, endpoint)


def get_page_statistics(self, _method, _endpoint, _qs) -> None:
    statistics_content = read_json_file(self, "visit_counters.json")
    print(statistics_content)
    today = datetime.today().date()
    day = str(today)
    stats = {}
    visit_count = 0
    for point in statistics_content:
        stats[point] = {}

        if day in statistics_content[point]:
            stats[point]["today"] = statistics_content[point].get(day, 0)
        visit_count = stats[point].get("today", 0)

        day = str(today - timedelta(days=1))
        if day in statistics_content[point]:
            stats[point]["yesterday"] = statistics_content[point].get(day, 0)
        visit_count += stats[point].get("yesterday", 0)

        for i in range(2, 6):
            day = str(today - timedelta(days=i))
            if day in statistics_content[point]:
                visit_count += statistics_content[point].get(day, 0)
        stats[point]["week"] = visit_count

        for i in range(7, 30):
            day = str(today - timedelta(days=i))
            if day in statistics_content[point]:
                visit_count += statistics_content[point].get(day, 0)
        stats[point]["month"] = visit_count

        day = str(today)
        visit_count = 0

    html = "<ul>"
    for endpoint, visits in stats.items():
        for data, count in visits.items():
            html += f"<li>{endpoint}:\n {data} - {count}</li>"
    html += "</ul>"
    msg = get_file_contents("pages/statistics.html").format(stats=html)
    respond_200(self, msg, "text/html")


def get_page_editing(self, method, endpoint, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": modify_project,
    }
    if method in switcher:
        switcher[method](self, endpoint, "contents/cv_resume.json", "pages/editing.html")
    else:
        raise MethodNotAllowed


def modify_project(self, _endpoint, _file_content, _file_html):
    project_content = get_user_data(self)
    print(project_content)


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