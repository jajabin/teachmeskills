import logging
import os
import re
import uuid
from pathlib import Path
from typing import Tuple

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import src.common.errors as errors
import src.common.instances as instances
import src.common.paths as paths
import src.common.responds as responds
import src.pages.statistics_page as stats
import src.utils.file_utils as fu
import src.utils.json_utils as ju
import src.utils.user_utils as uu
from src.common.night_mode import set_night_mode


@csrf_exempt
def handler_page_cv(request, **kwargs) -> HttpResponse:
    logging.debug(f"request = {request}")
    logging.debug(f"request.POST = {request.POST.get}")
    logging.debug(f"request.body = {request.body}")

    switcher = {
        r"^/cv\/project\/<str:project_id>\/\/(\w+)": get_page_cv_project,
        r"^/cv\/project\/<str:project_id>/": get_page_cv_project,
        r"^/cv\/project\/(\w+)/$": get_page_cv_project,
        r"^/cv\/projects\/editing/$": get_page_projects_editing,
        r"^/cv\/projects\/editing\/(\w+)$": get_page_projects_editing,
        r"^/cv\/projects/$": get_page_cv_projects,
        r"^/cv\/projects\/(\w+)$": get_page_cv_projects,
        r"^/cv\/education/$": get_page_cv_education,
        r"^/cv\/education\/(\w+)$": get_page_cv_education,
        r"^/cv\/skills/$": get_page_cv_skills,
        r"^/cv\/skills\/(\w+)$": get_page_cv_skills,
        r"^/cv\/job/$": get_page_cv_job,
        r"^/cv\/job\/(\w+)$": get_page_cv_job,
        r"^/cv/$": get_page_cv,
        r"^/cv\/(\w+)": get_page_cv,
    }
    function, _arguments = parse_endpoint(switcher, request.path)
    try:
        return function(request, **kwargs)
    except (FileNotFoundError, errors.PageNotFoundError):
        return responds.respond_404()
    except errors.MethodNotAllowed:
        return responds.respond_405()


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


def get_page_cv(request, **kwargs) -> HttpResponse:
    return get_page(request, None, paths.CV_HTML, **kwargs)


def get_page_cv_education(request, **kwargs) -> HttpResponse:
    return get_page(request, paths.CV_EDUCATION_JSON, paths.CV_EDUCATION_HTML, **kwargs)


def get_page_cv_job(request, **kwargs) -> HttpResponse:
    return get_page(request, paths.CV_JOB_JSON, paths.CV_JOB_HTML, **kwargs)


def get_page_cv_skills(request, **kwargs) -> HttpResponse:
    return get_page(request, paths.CV_SKILLS_JSON, paths.CV_SKILLS_HTML, **kwargs)


def get_page_cv_projects(request, **kwargs) -> HttpResponse:
    return get_page(request, paths.CV_PROJECTS_JSON, paths.CV_PROJECTS_HTML, **kwargs)


def get_page_projects_editing(request, **kwargs) -> HttpResponse:
    return get_page(request, paths.CV_PROJECTS_JSON, paths.CV_PROJECTS_EDITING_HTML, **kwargs)


def get_page_cv_project(request, **kwargs) -> HttpResponse:
    return get_page(request, paths.CV_PROJECTS_JSON, paths.CV_PROJECT_HTML, **kwargs)


@csrf_exempt
def get_page(request, file_content: Path, file_html: Path, **kwargs) -> HttpResponse:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if request.method in switcher:
        return switcher[request.method](request, request.path, file_content, file_html, **kwargs)
    else:
        raise errors.MethodNotAllowed


def show_page_cv(request, endpoint: str, file_content: str, file_html: str, **kwargs) -> HttpResponse:
    """
    show a page
    :param request: server instance
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

    user_id = uu.get_user_id(request)
    user_session = uu.read_user_session(user_id)

    cv_links = fu.get_file_contents(paths.CV_LINKS_HTML)

    projects = ""
    formaction = ""
    if endpoint == "/cv/projects/":
        for project in page_content:
            projects += "<h3>" + page_content[project][
                "project_name"] + f" (id: {project})     " + "<a href=/cv/project/" + project + ">Edit</a>" + "</h3>"
            projects += "<p>" + page_content[project]["project_date"] + "</p>"
            projects += "<p>" + page_content[project]["project_description"] + "</p>"
    if endpoint.startswith("/cv/project/"):
        project_id = kwargs[instances.PROJECT_ID]
        if project_id in page_content:
            projects += "<h3>" + page_content[project_id]["project_name"] + f" (id: {project_id})" + "</h3>"
            projects += "<p>" + page_content[project_id]["project_date"] + "</p>"
            projects += "<p>" + page_content[project_id]["project_description"] + "</p>"
            formaction = endpoint + "set_night_mode"


    msg = fu.get_file_contents(file_html) \
        .format(cv_links=cv_links, **resume_content, **page_content, projects=projects, **user_session[user_id], formaction=formaction)
    msg = fu.get_file_contents(paths.TEMPLATE_HTML).format(title="Resume", **user_session[user_id], body=msg)

    return responds.respond_200(msg)


@csrf_exempt
def save_page_cv(request, endpoint: str, file_content: Path, _file_html, **kwargs) -> HttpResponse:
    """
    save some settings
    :param request: server instance
    :param endpoint: current endpoint
    :param file_content: text content (for projects editing)
    :param _file_html: not used
    :return: nothing
    """

    if endpoint.startswith("/cv/project/"):
        redirect_to = "/cv/project/" + kwargs[instances.PROJECT_ID]
    else:
        redirect_to = instances.ENDPOINT_REDIRECTS[endpoint]

    logging.debug(f"redirect_to = {redirect_to}")

    switcher = {
        r"^/(.+)\/set_night_mode": set_night_mode,
        r"^/(.+)\/delete": remove_project,
        r"^/(.+)\/add": add_project,
        r"^/(.+)\/edit": edit_project,
    }
    function, _arguments = parse_endpoint(switcher, endpoint)
    try:
        return function(request, redirect_to, file_content)
    except (FileNotFoundError, errors.PageNotFoundError):
        return responds.respond_404()
    except errors.MethodNotAllowed:
        return responds.respond_405()


def edit_project(request, redirect_to, file_content: Path) -> HttpResponse:
    logging.debug(redirect_to)
    new_project_content = instances.NEW_PROJECT.copy()
    new_project_content.update(uu.parse_received_data(request))

    projects_content = ju.read_json_file(file_content)

    if instances.PROJECT_ID not in new_project_content:
        return responds.respond_418()
    if new_project_content[instances.PROJECT_ID] not in projects_content:
        return responds.respond_418()

    for item in new_project_content:
        if item != instances.PROJECT_ID:
            projects_content[new_project_content[instances.PROJECT_ID]][item] = new_project_content[item]

    ju.write_json_file(file_content, projects_content)
    return HttpResponseRedirect(redirect_to)


def add_project(request, redirect_to, file_content: Path) -> HttpResponse:
    projects_content = ju.read_json_file(file_content)
    new_project = instances.NEW_PROJECT.copy()
    new_project.update(uu.parse_received_data(request))

    new_project_id = os.urandom(16).hex()
    if new_project_id not in projects_content:
        projects_content[new_project_id] = {}

    projects_content[new_project_id].update(new_project)
    ju.write_json_file(file_content, projects_content)
    return HttpResponseRedirect(redirect_to)


def remove_project(request, redirect_to, file_content: Path) -> HttpResponse:
    project_content = instances.NEW_PROJECT.copy()
    project_content.update(uu.parse_received_data(request))

    projects_content = ju.read_json_file(file_content)

    if instances.PROJECT_ID not in project_content:
        return responds.respond_418()
    if project_content[instances.PROJECT_ID] not in projects_content:
        return responds.respond_418()

    projects_content.pop(project_content[instances.PROJECT_ID])
    ju.write_json_file(file_content, projects_content)
    return HttpResponseRedirect(redirect_to)
