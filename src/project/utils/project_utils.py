import os
from pathlib import Path
from typing import Dict, List

from project.utils import instances
from project.utils import user_utils as uu, json_utils as ju


def get_projects(page_content) -> List:
    projects = []
    for project in page_content:
        project = build_project(page_content, project)
        projects.append(project)
    return projects


def build_project(page_content, project) -> Dict:
    project = {instances.PROJECT_ID_key: project,
               instances.PROJECT_NAME_key: page_content[project][instances.PROJECT_NAME_key],
               instances.PROJECT_DATE_key: page_content[project][instances.PROJECT_DATE_key],
               instances.PROJECT_DESCRIPTION_key: page_content[project][instances.PROJECT_DESCRIPTION_key]}
    return project


def add_project(file_content: Path, project):
    projects_content = ju.read_json_file(file_content)
    new_project = instances.NEW_PROJECT.copy()
    new_project.update(project)

    new_project_id = os.urandom(16).hex()
    projects_content[new_project_id] = {}
    projects_content[new_project_id].update(new_project)
    ju.write_json_file(file_content, projects_content)


def remove_project(file_content: Path, project_id):
    projects_content = ju.read_json_file(file_content)
    projects_content.pop(project_id)
    ju.write_json_file(file_content, projects_content)


def edit_project(file_content: Path, project_id, project):
    new_project_content = instances.NEW_PROJECT.copy()
    new_project_content.update(project)

    projects_content = ju.read_json_file(file_content)
    projects_content[project_id].update(new_project_content)
    ju.write_json_file(file_content, projects_content)