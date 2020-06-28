import socketserver
import os
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from typing import Union, Dict
from src.errors import *
from src.json_utils import *
from src.cookies_utils import *


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
        "/goodbye": get_page_goodbye,
        "/cv": get_page_cv,
        "/cv/job": get_page_cv_job,
        "/cv/education": get_page_cv_education,
        "/cv/skills": get_page_cv_skills,
        "/cv/projects": get_page_cv_projects,
        "/statistics": get_page_statistics,
        "/cv/projects/additing": get_page_projects_editing,
        "/cv/projects/editing": get_page_projects_editing,
        "/cv/projects/removing": get_page_projects_editing,
        "/cv/projects/editing/add": get_page_projects_editing,
        "/cv/projects/editing/edit": get_page_projects_editing,
        "/cv/projects/editing/delete": get_page_projects_editing,
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

    user_session = read_user_session(self)

    msg = get_file_contents("pages/hello.html").format(**user_session)
    respond_200(self, msg, "text/html")


def read_user_session(self) -> Dict[str, str]:
    cookies_content = get_cookies(self)
    user_data = read_json_file("sessions.json")

    current_user_session = {}
    try:
        user_id = cookies_content["user_id"]
        current_user_session["name"] = user_data[user_id]["name"]
        today = datetime.today().year
        current_user_session["year"] = today - int(user_data[user_id]["age"])
        current_user_session["background_color"] = user_data[user_id]["background_color"]
        current_user_session["text_color"] = user_data[user_id]["text_color"]
    except KeyError:
        current_user_session["name"] = "Dude"
        current_user_session["year"] = "-"
        current_user_session["background_color"] = "white"
        current_user_session["text_color"] = "gray"

    return current_user_session


def save_user_data(self, _endpoint, _content_file):
    user_data = read_json_file("sessions.json")
    new_user_data = parse_user_sessions(self)

    new_user_data["background_color"] = "white"
    new_user_data["text_color"] = "gray"

    user_id = new_user_data["name"]     # now it's name
    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id].update(new_user_data)
    update_json_file(user_data, "sessions.json")

    cookie_master = set_cookies(self, {"user_id": user_id})

    respond_302(self, "/hello", cookie_master)


def increment_page_visit(self, endpoint: str) -> None:
    today = str(datetime.today().date())
    statistics_content = read_json_file("visit_counters.json")

    if endpoint not in statistics_content:
        statistics_content[endpoint] = {}
    if today not in statistics_content[endpoint]:
        statistics_content[endpoint][today] = 0

    statistics_content[endpoint][today] += 1
    write_json_file("visit_counters.json", statistics_content)


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


def get_page_goodbye(self, _method, endpoint: str, _qs) -> None:
    increment_page_visit(self, endpoint)
    today = datetime.today()
    phrase = say_bye(today.hour)

    user_session = read_user_session(self)

    msg = get_file_contents("pages/goodbye.html").format(date=today, phrase=phrase, **user_session)  # format ???
    respond_200(self, msg, "text/html")


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
        switcher[method](self, endpoint, None, "pages/cv.html")
    else:
        raise MethodNotAllowed


def get_page_cv_education(self, method: str, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "contents/cv_education.json", "pages/cv_education.html")
    else:
        raise MethodNotAllowed


def get_page_cv_job(self, method, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "contents/cv_job.json", "pages/cv_job.html")
    else:
        raise MethodNotAllowed


def get_page_cv_skills(self, method, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "contents/cv_skills.json", "pages/cv_skills.html")
    else:
        raise MethodNotAllowed


def get_page_cv_projects(self, method, endpoint, _qs) -> None:
    switcher = {
        "GET": show_page_cv_projects,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](self, endpoint, "contents/cv_projects.json", "pages/cv_projects.html")
    else:
        raise MethodNotAllowed


def show_page_cv_projects(self, endpoint: str, file_content: str, file_html: str):
    increment_page_visit(self, endpoint)

    resume_content = read_json_file("contents/cv_resume.json")
    projects_content = {}
    if file_content is not None:
        projects_content = read_json_file(file_content)

    user_session = read_user_session(self)

    cv_links = get_file_contents("pages/cv_links.html")

    projects = ""
    for project in projects_content:
        projects += "<h3>" + projects_content[project]["project_name"] + f" (id: {project})" + "</h3>"
        projects += "<p>" + projects_content[project]["project_date"] + "</p>"
        projects += "<p>" + projects_content[project]["project_description"] + "</p>"

    msg = get_file_contents("pages/header.html")
    msg += get_file_contents(file_html).format(cv_links=cv_links, **resume_content, projects=projects, **user_session)
    msg += get_file_contents("pages/footer.html")

    respond_200(self, msg, "text/html")


def show_page_cv(self, endpoint: str, file_content: str, file_html: str):
    increment_page_visit(self, endpoint)

    resume_content = read_json_file("contents/cv_resume.json")
    page_content = {}
    if file_content is not None:
        page_content = read_json_file(file_content)

    user_session = read_user_session(self)

    cv_links = get_file_contents("pages/cv_links.html")

    msg = get_file_contents("pages/header.html")
    msg += get_file_contents(file_html).format(cv_links=cv_links, **resume_content, **page_content, **user_session)
    msg += get_file_contents("pages/footer.html")

    respond_200(self, msg, "text/html")


def save_page_cv(self, endpoint: str, _file_content, _file_html):
    cookies_content = get_cookies(self)
    user_data = read_json_file("sessions.json")
    try:
        user_id = cookies_content["user_id"]
        user_data[user_id]["background_color"], user_data[user_id]["text_color"] = user_data[user_id]["text_color"], user_data[user_id]["background_color"]
    except KeyError:
        user_data[user_id]["background_color"], user_data[user_id]["text_color"] = "white", "gray"

    update_json_file(user_data, "sessions.json")

    respond_302(self, endpoint)


def calculate_stats(page_statistics, start_date, count_days) -> int:
    visit_counter = 0
    for day_counter in range(0, count_days + 1):
        day = str(start_date - timedelta(days=day_counter))
        if day in page_statistics:
            visit_counter += page_statistics[day]

    return visit_counter


def get_page_statistics(self, _method, _endpoint, _qs) -> None:
    statistics_content = read_json_file("visit_counters.json")

    today = datetime.today().date()
    stats = {}
    for page in statistics_content:
        stats[page] = {}
        stats[page]["today"] = calculate_stats(statistics_content[page], today, 0)
        stats[page]["yesterday"] = calculate_stats(statistics_content[page], today - timedelta(days=1), 0)
        stats[page]["week"] = calculate_stats(statistics_content[page], today, 7)
        stats[page]["month"] = calculate_stats(statistics_content[page], today, 30)

    html = """<tr>
            <th>Page</th>
            <th>Today</th>
            <th>Yesterday</th> 
            <th>Week</th>
            <th>Month</th>
           </tr>"""
    for endpoint, visits in stats.items():
        html += f"<tr><td>{endpoint}</td>"
        for data, count in visits.items():
            html += f"<td>{count}</td>"
    html += "</tr>"

    user_session = read_user_session(self)

    msg = get_file_contents("pages/statistics.html").format(stats=html, **user_session)
    respond_200(self, msg, "text/html")


def get_page_projects_editing(self, method, endpoint, _qs) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": modify_project,
    }
    if method in switcher:
        switcher[method](self, endpoint, "contents/cv_projects.json", "pages/cv_projects_editing.html")
    else:
        raise MethodNotAllowed


def modify_project(self, endpoint, file_content, _file_html) -> None:
    print("in modify_project: ", endpoint)
    switcher = {
        "/cv/projects/editing/add": add_project,
        "/cv/projects/editing/edit": edit_project,
        "/cv/projects/editing/delete": remove_project,
    }
    if endpoint in switcher:
        switcher[endpoint](self, file_content)
    else:
        raise MethodNotAllowed


# edit a project
def edit_project(self, file_content):
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
def add_project(self, file_content):
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
            new_project[id_new_project][item] = new_project_content[item] #dict.setdefault(key, default_value)

    projects_content.update(new_project)
    write_json_file(file_content, projects_content)
    respond_302(self, "/cv/projects")


# remove a project
def remove_project(self, file_content):
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
    msg = "Enter the correct ID Project"
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
        print(cookie_master)
        for item in cookie_master.values():
            self.send_header("Set-Cookie", item.OutputString())

    #self.send_header("Cache-Control", f"max-age={30 * 24 * 60 * 60}")

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