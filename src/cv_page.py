from src.errors import *
from src.statistics_page import *


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

    #cookie_master = set_cookies(self, {"user_id": user_id})
    #respond_200(self, msg, "text/html", cookie_master)
    respond_200(self, msg, "text/html")


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
