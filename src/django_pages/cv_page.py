import logging
import os
import re
import uuid
from pathlib import Path
from typing import Tuple

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import src.django_common.errors as errors
import src.django_common.instances as instances
import src.django_common.paths as paths
import src.django_common.responds as responds
import src.django_pages.statistics_page as stats
import src.django_utils.file_utils as fu
import src.django_utils.json_utils as ju
import src.django_utils.user_utils as uu
from src.django_common.night_mode import set_night_mode


@csrf_exempt
def handler_page_cv(request, **kwargs) -> HttpResponse:
    print(f"request = {request}")
    print(f"request.POST = {request.POST.get}")
    print(f"request.body = {request.body}")

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
        return function(request)
    except (FileNotFoundError, errors.PageNotFoundError):
        return responds.respond_404(request)
    except errors.MethodNotAllowed:
        return responds.respond_405(request)


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


def get_page_cv(request) -> HttpResponse:
    return get_page(request, None, paths.CV_HTML)


def get_page_cv_education(request) -> HttpResponse:
    return get_page(request, paths.CV_EDUCATION_JSON, paths.CV_EDUCATION_HTML)


def get_page_cv_job(request) -> HttpResponse:
    return get_page(request, paths.CV_JOB_JSON, paths.CV_JOB_HTML)


def get_page_cv_skills(request) -> HttpResponse:
    return get_page(request, paths.CV_SKILLS_JSON, paths.CV_SKILLS_HTML)


def get_page_cv_projects(request) -> HttpResponse:
    return get_page(request, paths.CV_PROJECTS_JSON, paths.CV_PROJECTS_HTML)


def get_page_projects_editing(request) -> HttpResponse:
    return get_page(request, paths.CV_PROJECTS_JSON, paths.CV_PROJECTS_EDITING_HTML)


def get_page_cv_project(request) -> HttpResponse:
    return get_page(request, paths.CV_PROJECTS_JSON, paths.CV_PROJECT_HTML)


@csrf_exempt
def get_page(request, file_content: Path, file_html: Path) -> HttpResponse:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if request.method in switcher:
        return switcher[request.method](request, request.path, file_content, file_html)
    else:
        raise errors.MethodNotAllowed


def show_page_cv(request, endpoint: str, file_content: str, file_html: str) -> HttpResponse:
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
        result = re.search("^/cv\/project\/(\w+)", endpoint)
        if result[1] in page_content:
            projects += "<h3>" + page_content[result[1]]["project_name"] + f" (id: {result[1]})" + "</h3>"
            projects += "<p>" + page_content[result[1]]["project_date"] + "</p>"
            projects += "<p>" + page_content[result[1]]["project_description"] + "</p>"
            formaction = endpoint + "set_night_mode"


    msg = fu.get_file_contents(file_html) \
        .format(cv_links=cv_links, **resume_content, **page_content, projects=projects, **user_session[user_id], formaction=formaction)
    msg = fu.get_file_contents(paths.TEMPLATE_HTML).format(title="Resume", **user_session[user_id], body=msg)

    return HttpResponse(msg)


@csrf_exempt
def save_page_cv(request, endpoint: str, file_content: Path, _file_html) -> HttpResponse:
    """
    save some settings
    :param request: server instance
    :param endpoint: current endpoint
    :param file_content: text content (for projects editing)
    :param _file_html: not used
    :return: nothing
    """

    if endpoint.startswith("/cv/project/"):
        path = endpoint.split("/") if '/' in endpoint else [endpoint, ""]
        redirect_to = "/cv/project/" + path[3]
    else:
        redirect_to = instances.ENDPOINT_REDIRECTS[endpoint]

    print(f"redirect_to = {redirect_to}")

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
        return function(request, redirect_to, file_content)
    except (FileNotFoundError, errors.PageNotFoundError):
        responds.respond_404(request)
    except errors.MethodNotAllowed:
        responds.respond_405(request)


def edit_project(request, redirect_to, file_content: Path) -> HttpResponse:
    logging.debug(redirect_to)
    new_project_content = instances.NEW_PROJECT
    new_project_content[instances.PROJECT_ID] = request.POST.get(instances.PROJECT_ID, "")
    new_project_content[instances.PROJECT_NAME_key] = request.POST.get(instances.PROJECT_NAME_key, "")
    new_project_content[instances.PROJECT_DATE_key] = request.POST.get(instances.PROJECT_DATE_key, "")
    new_project_content[instances.PROJECT_DESCRIPTION_key] = request.POST.get(instances.PROJECT_DESCRIPTION_key, "")

    projects_content = ju.read_json_file(file_content)

    if instances.PROJECT_ID not in new_project_content:
        return responds.respond_418(request)
    if new_project_content[instances.PROJECT_ID] not in projects_content:
        return responds.respond_418(request)

    for item in new_project_content:
        if item != instances.PROJECT_ID:
            projects_content[new_project_content[instances.PROJECT_ID]][item] = new_project_content[item]

    ju.write_json_file(file_content, projects_content)
    return HttpResponseRedirect(redirect_to)


def add_project(request, redirect_to, file_content: Path) -> None:
    projects_content = ju.read_json_file(file_content)
    new_project = instances.NEW_PROJECT
    new_project[instances.PROJECT_NAME_key] = request.POST.get(instances.PROJECT_NAME_key, "")
    new_project[instances.PROJECT_DATE_key] = request.POST.get(instances.PROJECT_DATE_key, "")
    new_project[instances.PROJECT_DESCRIPTION_key] = request.POST.get(instances.PROJECT_DESCRIPTION_key, "")

    new_project_id = os.urandom(16).hex()
    if new_project_id not in projects_content:
        projects_content[new_project_id] = {}

    projects_content[new_project_id].update(new_project)
    ju.write_json_file(file_content, projects_content)
    return HttpResponseRedirect(redirect_to)


def remove_project(request, redirect_to, file_content: Path) -> None:
    new_project_content = instances.NEW_PROJECT
    new_project_content[instances.PROJECT_ID] = request.POST.get(instances.PROJECT_ID, "")

    projects_content = ju.read_json_file(file_content)

    if instances.PROJECT_ID not in new_project_content:
        return responds.respond_418(request)
    if new_project_content[instances.PROJECT_ID] not in projects_content:
        return responds.respond_418(request)

    projects_content.pop(new_project_content[instances.PROJECT_ID])

    ju.write_json_file(file_content, projects_content)
    return HttpResponseRedirect(redirect_to)
