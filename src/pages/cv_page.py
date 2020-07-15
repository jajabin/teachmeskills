import logging
import os
import re
from pathlib import Path
from typing import Tuple

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import common.errors as errors
import common.instances as instances
import common.paths as paths
import common.responds as responds
import pages.statistics_page as stats
import utils.file_utils as fu
import utils.json_utils as ju
import utils.project_utils as pu
import utils.user_utils as uu
from common.night_mode import set_night_mode


@csrf_exempt
def get_page_cv(request) -> HttpResponse:
    return get_page(request, None, paths.CV_HTML)


@csrf_exempt
def get_page_cv_education(request) -> HttpResponse:
    return get_page(request, paths.CV_EDUCATION_JSON, paths.CV_EDUCATION_HTML)


@csrf_exempt
def get_page_cv_job(request) -> HttpResponse:
    return get_page(request, paths.CV_JOB_JSON, paths.CV_JOB_HTML)


@csrf_exempt
def get_page_cv_skills(request) -> HttpResponse:
    return get_page(request, paths.CV_SKILLS_JSON, paths.CV_SKILLS_HTML)


@csrf_exempt
def get_page_cv_projects(request) -> HttpResponse:
    return get_page(request, paths.CV_PROJECTS_JSON, paths.CV_PROJECTS_HTML)


@csrf_exempt
def get_page_projects_editing(request) -> HttpResponse:
    return get_page(request, paths.CV_PROJECTS_JSON, paths.CV_PROJECTS_ADDITING_HTML)


@csrf_exempt
def get_page_cv_project(request, project_id) -> HttpResponse:
    return get_page(request, paths.CV_PROJECTS_JSON, paths.CV_PROJECT_HTML, project_id)


@csrf_exempt
def get_page_cv_project_editing(request, project_id) -> HttpResponse:
    return get_page(request, paths.CV_PROJECTS_JSON, paths.CV_PROJECT_EDITING_HTML, project_id)


@require_http_methods(["GET", "POST"])
def get_page(request, file_content: Path, file_html: Path, project_id: str = None) -> HttpResponse:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }

    return switcher[request.method](request, request.path, file_content, file_html, project_id)


def show_page_cv(
        request,
        endpoint: str,
        file_content: str,
        file_html: str,
        project_id: str = None
) -> HttpResponse:
    """
    show a page
    :param request: server instance
    :param endpoint: current endpoint
    :param file_content: text content
    :param file_html: html code
    :param project_id: project ID
    :return: nothing
    """
    stats.increment_page_visit(endpoint)

    resume_content = ju.read_json_file(paths.CV_JSON)

    page_content = {}
    if file_content is not None:
        page_content = ju.read_json_file(file_content)

    projects = pu.get_projects(endpoint, page_content, project_id)

    user_id = uu.get_user_id(request)
    user_session = uu.read_user_session(user_id)

    cv_links = fu.get_file_contents(paths.CV_LINKS_HTML)

    return responds.respond_200(request, file_html, {"action_night_mode": endpoint + "set_night_mode/",
                                                     "cv_links": cv_links,
                                                     **resume_content,
                                                     **page_content,
                                                     "projects": projects,
                                                     **user_session[user_id]})


def save_page_cv(
        request,
        endpoint: str,
        file_content: Path,
        _file_html,
        project_id: str = None
) -> HttpResponse:
    """
    save some settings
    :param request: server instance
    :param endpoint: current endpoint
    :param file_content: text content (for projects editing)
    :param _file_html: not used
    :param project_id: project ID
    :return: nothing
    """

    redirect_to = get_redirect_to(endpoint, project_id)
    logging.debug(f"redirect_to = {redirect_to}")

    switcher = {
        r"^/(.+)\/set_night_mode/": set_night_mode,
        r"^/(.+)\/delete": remove_project,
        r"^/(.+)\/add": add_project,
        r"^/(.+)\/edit": edit_project,
    }
    function, _arguments = parse_endpoint(switcher, endpoint)
    try:
        return function(request, redirect_to, file_content, project_id)
    except (FileNotFoundError, errors.PageNotFoundError):
        return responds.respond_404()


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


def get_redirect_to(endpoint, project_id: str = None) -> str:
    if endpoint in instances.ENDPOINT_REDIRECTS:
        return instances.ENDPOINT_REDIRECTS[endpoint]

    if endpoint.startswith("/cv/project/"):
        if endpoint.endswith("/delete"):
            return "/cv/projects/"
        return "/cv/project/" + project_id

    return responds.respond_404()


def edit_project(request, redirect_to, file_content: Path, project_id) -> HttpResponse:
    logging.debug(redirect_to)
    new_project_content = instances.NEW_PROJECT.copy()
    new_project_content.update(uu.parse_received_data(request))

    projects_content = ju.read_json_file(file_content)

    for item in new_project_content:
        if item != instances.PROJECT_ID:
            projects_content[project_id][item] = new_project_content[item]

    ju.write_json_file(file_content, projects_content)
    return HttpResponseRedirect(redirect_to)


def add_project(request, redirect_to, file_content: Path, _project_id) -> HttpResponse:
    projects_content = ju.read_json_file(file_content)
    new_project = instances.NEW_PROJECT.copy()
    new_project.update(uu.parse_received_data(request))

    new_project_id = os.urandom(16).hex()
    if new_project_id not in projects_content:
        projects_content[new_project_id] = {}

    projects_content[new_project_id].update(new_project)
    ju.write_json_file(file_content, projects_content)

    return HttpResponseRedirect(redirect_to)


def remove_project(_request, redirect_to, file_content: Path, project_id) -> HttpResponse:
    projects_content = ju.read_json_file(file_content)

    if project_id is None:
        return responds.respond_418()

    projects_content.pop(project_id)
    ju.write_json_file(file_content, projects_content)
    return HttpResponseRedirect(redirect_to)

