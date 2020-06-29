import socketserver
import os
import uuid
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from typing import Union, Dict
from src.errors import *
from src.json_utils import *
from src.cookies_utils import *
from src.statistics_page import *
from src.goodbye_page import *

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
        "/hello/set_night_mode": get_page_hello,
        "/goodbye": get_page_goodbye,
        "/goodbye/set_night_mode": get_page_goodbye,
        "/cv": get_page_cv,
        "/cv/set_night_mode": get_page_cv,
        "/cv/job": get_page_cv_job,
        "/cv/job/set_night_mode": get_page_cv_job,
        "/cv/education": get_page_cv_education,
        "/cv/education/set_night_mode": get_page_cv_education,
        "/cv/skills": get_page_cv_skills,
        "/cv/skills/set_night_mode": get_page_cv_skills,
        "/cv/projects": get_page_cv_projects,
        "/cv/projects/set_night_mode": get_page_cv_projects,
        "/statistics": get_page_statistics,
        "/statistics/set_night_mode": get_page_statistics,
        "/cv/projects/editing": get_page_projects_editing,
        "/cv/projects/editing/add": get_page_projects_editing,
        "/cv/projects/editing/edit": get_page_projects_editing,
        "/cv/projects/editing/delete": get_page_projects_editing,
        "/cv/projects/editing/set_night_mode": get_page_projects_editing,
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
            raise PageNotFoundError
    except (FileNotFoundError, PageNotFoundError):
        respond_404(self)
    except MethodNotAllowed:
        respond_405(self)
    except MissingData:
        respond_418(self)


def get_page_hello(self, method: str, endpoint: str, qs: str) -> None:
    switcher = {
        "GET": show_page_hello,
        "POST": save_user_data,
    }
    if method in switcher:
        switcher[method](self, endpoint, "sessions.json")
    else:
        raise MethodNotAllowed


def show_page_hello(self, endpoint: str, _content_file):
    increment_page_visit(self, endpoint)

    user_id = get_user_id(self)
    user_session = read_user_session(self, user_id)
    cookie_master = set_cookies(self, {"user_id": user_id})

    msg = get_file_contents("pages/hello.html").format(**user_session[user_id])
    respond_200(self, msg, "text/html", cookie_master)


def get_user_id(self) -> str:
    cookies_content = get_cookies(self)
    try:
        return cookies_content["user_id"]
    except:
        return str(uuid.uuid1())


def read_user_session(self, user_id: str) -> Dict[str, str]:
    user_data = read_json_file("sessions.json")

    current_user_session = {}
    if user_id in user_data:
        current_user_session[user_id] = user_data[user_id]
        today = datetime.today().year
        current_user_session[user_id]["year"] = today - int(current_user_session[user_id]["age"]) if \
        current_user_session[user_id]["age"] != "-" else "-"
    else:
        current_user_session[user_id] = create_new_user_session()
        user_data.update(current_user_session)
        update_json_file(user_data, "sessions.json")

    return current_user_session


def create_new_user_session() -> Dict[str, str]:
    temp_user_data = {}
    temp_user_data["name"] = "Dude"
    temp_user_data["age"] = "-"
    temp_user_data["year"] = "-"
    temp_user_data["background_color"] = "white"
    temp_user_data["text_color"] = "gray"
    return temp_user_data


def save_user_data(self, endpoint: str, _content_file) -> None:
    switcher = {
        "/hello/set_night_mode": set_night_mode,
        "/hello/save": write_user_data,
    }
    if endpoint in switcher:
        switcher[endpoint](self, "/hello")
    else:
        raise MethodNotAllowed


def write_user_data(self, _endpoint, _content_file):
    user_data = read_json_file("sessions.json")
    new_user_data = parse_user_sessions(self)

    if "name" not in new_user_data:
        raise MissingData

    user_id = str(uuid.uuid1())
    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id].update(new_user_data)
    today = datetime.today().year
    user_data[user_id]["year"] = today - int(user_data[user_id]["age"]) if "age" in new_user_data else "-"
    user_data[user_id]["background_color"] = "white"
    user_data[user_id]["text_color"] = "gray"

    update_json_file(user_data, "sessions.json")
    cookie_master = set_cookies(self, {"user_id": user_id})

    respond_302(self, "/hello", cookie_master)


def parse_user_sessions(self) -> Dict[str, str]:
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


def get_cv_style(self, _method) -> None:
    msg = get_file_contents("pages/cv_style.css")
    respond_200(self, msg, "text/css")


def get_page_cv(self, method: str, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "/cv", None, "pages/cv.html")
    else:
        raise MethodNotAllowed


def get_page_cv_education(self, method: str, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "/cv/education", "contents/cv_education.json", "pages/cv_education.html")
    else:
        raise MethodNotAllowed


def get_page_cv_job(self, method, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "/cv/job", "contents/cv_job.json", "pages/cv_job.html")
    else:
        raise MethodNotAllowed


def get_page_cv_skills(self, method, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "/cv/skills", "contents/cv_skills.json", "pages/cv_skills.html")
    else:
        raise MethodNotAllowed


def get_page_cv_projects(self, method, endpoint, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "/cv/projects", "contents/cv_projects.json", "pages/cv_projects.html")
    else:
        raise MethodNotAllowed


def show_page_cv(self, endpoint: str, _redirect_to, file_content: str, file_html: str):
    increment_page_visit(self, endpoint)

    resume_content = read_json_file("contents/cv_resume.json")
    page_content = {}
    if file_content is not None:
        page_content = read_json_file(file_content)

    user_id = get_user_id(self)
    user_session = read_user_session(self, user_id)

    cv_links = get_file_contents("pages/cv_links.html")

    projects = ""
    if endpoint == "/cv/projects":
        for project in page_content:
            projects += "<h3>" + page_content[project]["project_name"] + f" (id: {project})" + "</h3>"
            projects += "<p>" + page_content[project]["project_date"] + "</p>"
            projects += "<p>" + page_content[project]["project_description"] + "</p>"

    msg = get_file_contents("pages/header.html")
    msg += get_file_contents(file_html) \
                .format(cv_links=cv_links, **resume_content, **page_content, projects=projects, **user_session[user_id])
    msg += get_file_contents("pages/footer.html")

    cookie_master = set_cookies(self, {"user_id": user_id})
    respond_200(self, msg, "text/html", cookie_master)


def set_night_mode(self, endpoint: str, _file_content=""):
    user_id = get_user_id(self)
    user_session = read_user_session(self, user_id)
    user_session[user_id]["background_color"], user_session[user_id]["text_color"] = \
                                        user_session[user_id]["text_color"], user_session[user_id]["background_color"]
    update_json_file(user_session, "sessions.json")
    cookie_master = set_cookies(self, {"user_id": user_id})
    respond_302(self, endpoint, cookie_master)


def save_page_cv(self, endpoint: str, redirect_to: str, _file_content, _file_html):
    switcher = {
        "/cv/set_night_mode": set_night_mode,
        "/cv/job/set_night_mode": set_night_mode,
        "/cv/education/set_night_mode": set_night_mode,
        "/cv/skills/set_night_mode": set_night_mode,
        "/cv/projects/set_night_mode": set_night_mode,
    }
    if endpoint in switcher:
        switcher[endpoint](self, redirect_to)
    else:
        raise MethodNotAllowed


def get_page_projects_editing(self, method, endpoint, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": modify_project,
    }
    if method in switcher:
        switcher[method](self, endpoint, "/cv/projects/editing", "contents/cv_projects.json", "pages/cv_projects_editing.html")
    else:
        raise MethodNotAllowed


def modify_project(self, endpoint, redirect_to, file_content, _file_html) -> None:
    switcher = {
        "/cv/projects/editing/add": add_project,
        "/cv/projects/editing/edit": edit_project,
        "/cv/projects/editing/delete": remove_project,
        "/cv/projects/editing/set_night_mode": set_night_mode,
    }
    if endpoint in switcher:
        switcher[endpoint](self, redirect_to, file_content)
    else:
        raise MethodNotAllowed


# edit a project
def edit_project(self, _redirect_to, file_content):
    print("in edit_project")
    new_project_content = parse_user_sessions(self)
    projects_content = read_json_file(file_content)

    if "project_id" not in new_project_content:
        raise MissingData
    if new_project_content["project_id"] not in projects_content:
        raise MissingData

    for item in new_project_content:
        if item != "project_id":
            projects_content[new_project_content["project_id"]][item] = new_project_content[item]

    write_json_file(file_content, projects_content)
    respond_302(self, "/cv/projects")


# add a new project
def add_project(self, _redirect_to, file_content):
    new_project_content = parse_user_sessions(self)
    projects_content = read_json_file(file_content)
    new_project = {}

    if "project_id" not in new_project_content:
        raise MissingData
    if new_project_content["project_id"] is projects_content:
        raise MissingData
    id_new_project = new_project_content["project_id"]
    new_project[id_new_project] = {"project_name": "", "project_date": "", "project_description": ""}

    for item in new_project_content:
        if item in new_project[id_new_project]:
            new_project[id_new_project][item] = new_project_content[item]  # dict.setdefault(key, default_value)

    projects_content.update(new_project)
    write_json_file(file_content, projects_content)
    respond_302(self, "/cv/projects")


# remove a project
def remove_project(self, _redirect_to, file_content):
    new_project_content = parse_user_sessions(self)
    projects_content = read_json_file(file_content)

    if "project_id" not in new_project_content:
        raise MissingData
    if new_project_content["project_id"] not in projects_content:
        raise MissingData

    projects_content.pop(new_project_content["project_id"])

    write_json_file(file_content, projects_content)
    respond_302(self, "/cv/projects")


def get_file_contents(file_path) -> str:
    full_file_path = Path(__file__).parent.parent.resolve() / file_path  # full path to dir where file is located
    if not full_file_path.is_file():
        raise FileNotFoundError
    with full_file_path.open("r", encoding="utf-8") as file_src:
        content = file_src.read()
    return content


def respond_200(self, msg: str, content_type="text/plain", cookies_content="") -> None:
    send_response(self, 200, msg, content_type, cookie_master=cookies_content)


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
    send_response(self, 302, "", "text/plain", redirect_to, cookie_master=cookies_content)


def send_response(self, code: int, msg: str, content_type: str, redirect_to="", cookie_master="") -> None:
    msg = msg.encode()

    self.send_response(code)
    self.send_header("Content-type", content_type)

    if redirect_to != "":
        self.send_header("Location", redirect_to)

    self.send_header("Content-length", len(msg))

    if cookie_master != "":
        for item in cookie_master.values():
            self.send_header("Set-Cookie", item.OutputString())

    # self.send_header("Cache-Control", f"max-age={30 * 24 * 60 * 60}")

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
