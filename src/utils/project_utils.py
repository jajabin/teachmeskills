from typing import Dict, List

from common import instances


def get_projects(endpoint, page_content, project_id: str = None) -> List:
    if not endpoint.startswith("/cv/project"):
        return []

    if project_id is not None:
        return [build_project(page_content, project_id)]

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
