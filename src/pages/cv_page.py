import logging
import os
import re
import uuid
from pathlib import Path
from typing import Tuple

import src.common.errors as errors
import src.common.instances as instances
import src.common.paths as paths
import src.common.responds as responds
import src.pages.statistics_page as stats
import src.utils.file_utils as fu
import src.utils.json_utils as ju
import src.utils.user_utils as uu
from src.common.night_mode import set_night_mode


def handler_page_cv(server_inst, method: str, endpoint: str, qs) -> None:
    #   regex r"cv\/projects\/(\w+)\/(\w+)"
    switcher = {
        #r"^/cv$": get_page_cv,
        #r"^/cv\/set_night_mode$": get_page_cv,
        #r"^/cv\/job$": get_page_cv_job,
        #r"^/cv\/job\/set_night_mode$": get_page_cv_job,
        #r"^/cv\/skills$": get_page_cv_skills,
        #r"^/cv\/skills\/set_night_mode$": get_page_cv_skills,
        #r"^/cv\/education$": get_page_cv_education,
        #r"^/cv\/education\/set_night_mode$": get_page_cv_education,
        #r"^/cv\/projects$": get_page_cv_projects,
        #r"^/cv\/projects\/set_night_mode$": get_page_cv_projects,
        #r"^\/cv\/projects\/editing": get_page_projects_editing,
        #r"^/cv\/projects\/editing$": get_page_projects_editing,
        #r"^/cv\/projects\/editing\/add$": get_page_projects_editing,
        #r"^/cv\/projects\/editing\/edit$": get_page_projects_editing,
        #r"^/cv\/projects\/editing\/delete$": get_page_projects_editing,
        #r"^/cv\/projects\/editing\/set_night_mode$": get_page_projects_editing,
        # r"^/cv\/project\/(\w+)\/set_night_mode$": get_page_cv_project,
        r"^/cv\/project\/(\w+)": get_page_cv_project,
        r"^/cv\/project\/(\w+)\/(\w+)": get_page_cv_project,
        r"^/cv\/projects\/editing$": get_page_projects_editing,
        r"^/cv\/projects\/editing\/(\w+)$": get_page_projects_editing,
        r"^/cv\/projects$": get_page_cv_projects,
        r"^/cv\/projects\/(\w+)$": get_page_cv_projects,
        r"^/cv\/education$": get_page_cv_education,
        r"^/cv\/education\/(\w+)$": get_page_cv_education,
        r"^/cv\/skills$": get_page_cv_skills,
        r"^/cv\/skills\/(\w+)$": get_page_cv_skills,
        r"^/cv\/job$": get_page_cv_job,
        r"^/cv\/job\/(\w+)$": get_page_cv_job,
        r"^/cv$": get_page_cv,
        r"^/cv\/(\w+)$": get_page_cv,
    }
    function, _arguments = parse_endpoint(switcher, endpoint)
    try:
        function(server_inst, method, endpoint, qs)
    except (FileNotFoundError, errors.PageNotFoundError):
        responds.respond_404(server_inst)
    except errors.MethodNotAllowed:
        responds.respond_405(server_inst)


def parse_endpoint(endpoints_dict, endpoint) -> Tuple:
    function = None
    arguments = {}

    for path, func in endpoints_dict.items():
        match = re.match(path, endpoint)
        if not match:
            continue

        function = func
        arguments = match.groupdict().copy()
        break

    if not function:
        raise errors.UnknownPath(endpoint)

    return function, arguments


def get_page_cv(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, None, paths.CV_HTML)


def get_page_cv_education(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, paths.CV_EDUCATION_JSON, paths.CV_EDUCATION_HTML)


def get_page_cv_job(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, paths.CV_JOB_JSON, paths.CV_JOB_HTML)


def get_page_cv_skills(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, paths.CV_SKILLS_JSON, paths.CV_SKILLS_HTML)


def get_page_cv_projects(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, paths.CV_PROJECTS_JSON, paths.CV_PROJECTS_HTML)


def get_page_projects_editing(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, paths.CV_PROJECTS_JSON,
             paths.CV_PROJECTS_EDITING_HTML)


def get_page_cv_project(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, paths.CV_PROJECTS_JSON,
             paths.CV_PROJECT_HTML)


def get_page(server_inst, method: str, endpoint: str, file_content: Path, file_html: Path) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](server_inst, endpoint, file_content, file_html)
    else:
        raise errors.MethodNotAllowed


def show_page_cv(server_inst, endpoint: str, file_content: str, file_html: str) -> None:
    """
    show a page
    :param server_inst: server instance
    :param endpoint: current endpoint
    :param file_content: text content
    :param file_html: html code
    :return: nothing
    """
    stats.increment_page_visit(endpoint)

    resume_content = ju.read_json_file(paths.CV_JSON)
    page_content = {}
    if file_content is not None:
        page_content = ju.read_json_file(file_content)

    user_id = uu.get_user_id(server_inst)
    user_session = uu.read_user_session(user_id)

    cv_links = fu.get_file_contents(paths.CV_LINKS_HTML)

    projects = ""
    formaction = ""
    if endpoint == "/cv/projects":
        for project in page_content:
            projects += "<h3>" + page_content[project][
                "project_name"] + f" (id: {project})     " + "<a href=/cv/project/" + project + ">Edit</a>" + "</h3>"
            projects += "<p>" + page_content[project]["project_date"] + "</p>"
            projects += "<p>" + page_content[project]["project_description"] + "</p>"
    if endpoint.startswith("/cv/project/"):
        result = re.search("^/cv\/project\/(\w+)", endpoint)
        if result[1] in page_content:
            projects += "<h3>" + page_content[result[1]]["project_name"] + f" (id: {result[1]})" + "</h3>"
            projects += "<p>" + page_content[result[1]]["project_date"] + "</p>"
            projects += "<p>" + page_content[result[1]]["project_description"] + "</p>"
            formaction = endpoint + "/set_night_mode"


    msg = fu.get_file_contents(file_html) \
        .format(cv_links=cv_links, **resume_content, **page_content, projects=projects, **user_session[user_id], formaction=formaction)
    msg = fu.get_file_contents(paths.TEMPLATE_HTML).format(title="Resume", **user_session[user_id], body=msg)

    # cookie_master = set_cookies(server_inst, {"user_id": user_id})
    # respond_200(server_inst, msg, "text/html", cookie_master)
    responds.respond_200(server_inst, msg, "text/html")


def save_page_cv(server_inst, endpoint: str, file_content: Path, _file_html) -> None:
    """
    save some settings
    :param server_inst: server instance
    :param endpoint: current endpoint
    :param file_content: text content (for projects editing)
    :param _file_html: not used
    :return: nothing
    """

    #redirect_to = instances.ENDPOINT_REDIRECTS[endpoint]

    # switcher = {
    #     "/cv/set_night_mode": set_night_mode,
    #     "/cv/job/set_night_mode": set_night_mode,
    #     "/cv/education/set_night_mode": set_night_mode,
    #     "/cv/skills/set_night_mode": set_night_mode,
    #     "/cv/projects/set_night_mode": set_night_mode,
    #     "/cv/projects/editing/add": add_project,
    #     "/cv/projects/editing/edit": edit_project,
    #     "/cv/projects/editing/delete": remove_project,
    #     "/cv/projects/editing/set_night_mode": set_night_mode
    # }
    # if endpoint in switcher:
    #     switcher[endpoint](server_inst, redirect_to, file_content)
    # else:
    #     raise errors.MethodNotAllowed

    if endpoint.startswith("/cv/project/"):
        path = endpoint.split("/") if '/' in endpoint else [endpoint, ""]
        redirect_to = "/cv/project/" + path[3]
    else:
        redirect_to = instances.ENDPOINT_REDIRECTS[endpoint]

    switcher = {
        r"^/(\w+)\/set_night_mode": set_night_mode,
        r"^/(\w+)\/(\w+)\/set_night_mode": set_night_mode,
        r"^/(\w+)\/(\w+)\/(\w+)\/set_night_mode": set_night_mode,
        r"^/(\w+)\/(\w+)\/(\w+)\/add": add_project,
        r"^/(\w+)\/(\w+)\/(\w+)\/edit": edit_project,
        r"^/(\w+)\/(\w+)\/(\w+)\/delete": remove_project,
    }
    function, _arguments = parse_endpoint(switcher, endpoint)
    try:
        function(server_inst, redirect_to, file_content)
    except (FileNotFoundError, errors.PageNotFoundError):
        responds.respond_404(server_inst)
    except errors.MethodNotAllowed:
        responds.respond_405(server_inst)


def edit_project(server_inst, redirect_to, file_content: Path) -> None:
    logging.debug(redirect_to)
    new_project_content = uu.parse_received_data(server_inst)
    projects_content = ju.read_json_file(file_content)

    if instances.PROJECT_ID not in new_project_content:
        responds.respond_418(server_inst)
    if new_project_content[instances.PROJECT_ID] not in projects_content:
        responds.respond_418(server_inst)

    for item in new_project_content:
        if item != instances.PROJECT_ID:
            projects_content[new_project_content[instances.PROJECT_ID]][item] = new_project_content[item]

    ju.write_json_file(file_content, projects_content)
    responds.respond_302(server_inst, redirect_to)


def add_project(server_inst, redirect_to, file_content: Path) -> None:
    projects_content = ju.read_json_file(file_content)
    new_project = instances.NEW_PROJECT
    new_project.update(uu.parse_received_data(server_inst))

    new_project_id = os.urandom(16).hex()
    if new_project_id not in projects_content:
        projects_content[new_project_id] = {}

    projects_content[new_project_id].update(new_project)
    ju.write_json_file(file_content, projects_content)
    responds.respond_302(server_inst, redirect_to)


def remove_project(server_inst, redirect_to, file_content: Path) -> None:
    new_project_content = uu.parse_received_data(server_inst)
    projects_content = ju.read_json_file(file_content)

    if instances.PROJECT_ID not in new_project_content:
        responds.respond_418(server_inst)
    if new_project_content[instances.PROJECT_ID] not in projects_content:
        responds.respond_418(server_inst)

    projects_content.pop(new_project_content[instances.PROJECT_ID])

    ju.write_json_file(file_content, projects_content)
    responds.respond_302(server_inst, redirect_to)
