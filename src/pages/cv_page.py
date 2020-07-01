from pathlib import Path

import src.common.errors as errors
import src.common.instances as instances
import src.common.night_mode as nm
import src.common.paths as paths
import src.common.responds as responds
import src.pages.statistics_page as stats
import src.utils.file_utils as fu
import src.utils.json_utils as ju
import src.utils.user_utils as uu


def get_page_cv(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, "/cv", None, paths.CV_HTML)


def get_page_cv_education(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, "/cv/education", paths.CV_EDUCATION_JSON, paths.CV_EDUCATION_HTML)


def get_page_cv_job(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, "/cv/job", paths.CV_JOB_JSON, paths.CV_JOB_HTML)


def get_page_cv_skills(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, "/cv/skills", paths.CV_SKILLS_JSON, paths.CV_SKILLS_HTML)


def get_page_cv_projects(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, "/cv/projects", paths.CV_PROJECTS_JSON, paths.CV_PROJECTS_HTML)


def get_page_projects_editing(server_inst, method: str, endpoint: str, _qs) -> None:
    get_page(server_inst, method, endpoint, "/cv/projects/editing", paths.CV_PROJECTS_JSON, paths.CV_PROJECTS_EDITING_HTML)


def get_page(server_inst, method: str, endpoint: str, redirect_to: str, file_content: Path, file_html: Path) -> None:
    switcher = {
        "GET": show_page_cv,
        "POST": save_page_cv,
    }
    if method in switcher:
        switcher[method](server_inst, endpoint, redirect_to, file_content, file_html)
    else:
        raise errors.MethodNotAllowed


def show_page_cv(server_inst, endpoint: str, _redirect_to, file_content: str, file_html: str) -> None:
    """
    show a page
    :param server_inst: server instance
    :param endpoint: current endpoint
    :param _redirect_to: not used
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
    if endpoint == "/cv/projects":
        for project in page_content:
            projects += "<h3>" + page_content[project]["project_name"] + f" (id: {project})" + "</h3>"
            projects += "<p>" + page_content[project]["project_date"] + "</p>"
            projects += "<p>" + page_content[project]["project_description"] + "</p>"

    msg = fu.get_file_contents(paths.HEADER_HTML)
    msg += fu.get_file_contents(file_html) \
        .format(cv_links=cv_links, **resume_content, **page_content, projects=projects, **user_session[user_id])
    msg += fu.get_file_contents(paths.FOOTER_HTML)

    # cookie_master = set_cookies(server_inst, {"user_id": user_id})
    # respond_200(server_inst, msg, "text/html", cookie_master)
    responds.respond_200(server_inst, msg, "text/html")


def save_page_cv(server_inst, endpoint: str, redirect_to: str, file_content: Path, _file_html) -> None:
    """
    save some settings
    :param server_inst: server instance
    :param endpoint: current endpoint
    :param redirect_to: where to redirect
    :param file_content: text content (for projects editing)
    :param _file_html: not used
    :return: nothing
    """
    switcher = {
        "/cv/set_night_mode": nm.set_night_mode,
        "/cv/job/set_night_mode": nm.set_night_mode,
        "/cv/education/set_night_mode": nm.set_night_mode,
        "/cv/skills/set_night_mode": nm.set_night_mode,
        "/cv/projects/set_night_mode": nm.set_night_mode,
        "/cv/projects/editing/add": add_project,
        "/cv/projects/editing/edit": edit_project,
        "/cv/projects/editing/delete": remove_project,
        "/cv/projects/editing/set_night_mode": nm.set_night_mode,
    }
    if endpoint in switcher:
        switcher[endpoint](server_inst, redirect_to, file_content)
    else:
        raise errors.MethodNotAllowed


def edit_project(server_inst, _redirect_to, file_content: Path) -> None:
    new_project_content = uu.parse_received_data(server_inst)
    projects_content = ju.read_json_file(file_content)

    if "project_id" not in new_project_content:
        responds.respond_418(server_inst)
    if new_project_content["project_id"] not in projects_content:
        responds.respond_418(server_inst)

    for item in new_project_content:
        if item != "project_id":
            projects_content[new_project_content["project_id"]][item] = new_project_content[item]

    ju.write_json_file(file_content, projects_content)
    responds.respond_302(server_inst, "/cv/projects")


def add_project(server_inst, _redirect_to, file_content: Path) -> None:
    new_project_content = uu.parse_received_data(server_inst)
    projects_content = ju.read_json_file(file_content)
    new_project = {}

    if "project_id" not in new_project_content:
        responds.respond_418(server_inst)
    if new_project_content["project_id"] is projects_content:
        responds.respond_418(server_inst)
    id_new_project = new_project_content["project_id"]
    new_project[id_new_project] = instances.NEW_PROJECT

    for item in new_project_content:
        if item in new_project[id_new_project]:
            new_project[id_new_project][item] = new_project_content[item]  # dict.setdefault(key, default_value)

    projects_content.update(new_project)
    ju.write_json_file(file_content, projects_content)
    responds.respond_302(server_inst, "/cv/projects")


def remove_project(server_inst, _redirect_to, file_content: Path) -> None:
    new_project_content = uu.parse_received_data(server_inst)
    projects_content = ju.read_json_file(file_content)

    if "project_id" not in new_project_content:
        responds.respond_418(server_inst)
    if new_project_content["project_id"] not in projects_content:
        responds.respond_418(server_inst)

    projects_content.pop(new_project_content["project_id"])

    ju.write_json_file(file_content, projects_content)
    responds.respond_302(server_inst, "/cv/projects")
