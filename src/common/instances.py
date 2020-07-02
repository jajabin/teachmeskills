import src.common.night_mode


PROJECT_ID = "project_id"
USER_ID = "user_id"

DARK_COLOR = "gray"
LIGHT_COLOR = "white"

COOKIE_TERM = 30

NAME_key = "name"
AGE_key = "age"
YEAR_key = "year"
BCKG_COLOR = "background_color"
TXT_COLOR = "text_color"

PROJECT_NAME_key = "project_name"
PROJECT_DATE_key = "project_date"
PROJECT_DESCRIPTION_key = "project_description"

NEW_USER = {NAME_key: "Dude", AGE_key: "", YEAR_key: "", BCKG_COLOR: LIGHT_COLOR, TXT_COLOR: DARK_COLOR}
NEW_PROJECT = {PROJECT_NAME_key: "", PROJECT_DATE_key: "", PROJECT_DESCRIPTION_key: ""}

ENDPOINT_FUNCTIONS = {
      "/hello": "get_page_hello",
      "/hello/save": "get_page_hello",
      "/hello/set_night_mode": "get_page_hello",
      "/goodbye": "get_page_goodbye",
      "/goodbye/set_night_mode": "get_page_goodbye",
      "/cv": "get_page_cv",
      "/cv/set_night_mode": "get_page_cv",
      "/cv/job": "get_page_cv_job",
      "/cv/job/set_night_mode": "get_page_cv_job",
      "/cv/education": "get_page_cv_education",
      "/cv/education/set_night_mode": "get_page_cv_education",
      "/cv/skills": "get_page_cv_skills",
      "/cv/skills/set_night_mode": "get_page_cv_skills",
      "/cv/projects": "get_page_cv_projects",
      "/cv/projects/set_night_mode": "get_page_cv_projects",
      "/statistics": "get_page_statistics",
      "/statistics/set_night_mode": "get_page_statistics",
      "/cv/projects/editing": "get_page_projects_editing",
      "/cv/projects/editing/add": "get_page_projects_editing",
      "/cv/projects/editing/edit": "get_page_projects_editing",
      "/cv/projects/editing/delete": "get_page_projects_editing",
      "/cv/projects/editing/set_night_mode": "get_page_projects_editing"
}

ENDPOINT_REDIRECTS = {
      "/hello": "/hello",
      "/hello/save": "/hello",
      "/hello/set_night_mode": "/hello",
      "/goodbye": "/goodbye",
      "/goodbye/set_night_mode": "/goodbye",
      "/cv": "/cv",
      "/cv/set_night_mode": "/cv",
      "/cv/job": "/cv/job",
      "/cv/job/set_night_mode": "/cv/job",
      "/cv/education": "/cv/education",
      "/cv/education/set_night_mode": "/cv/education",
      "/cv/skills": "/cv/skills",
      "/cv/skills/set_night_mode": "/cv/skills",
      "/cv/projects": "/cv/projects",
      "/cv/projects/set_night_mode": "/cv/projects",
      "/statistics": "/statistics",
      "/statistics/set_night_mode": "/statistics",
      "/cv/projects/editing": "/cv/projects/editing",
      "/cv/projects/editing/add": "/cv/projects",
      "/cv/projects/editing/edit": "/cv/projects",
      "/cv/projects/editing/delete": "/cv/projects",
      "/cv/projects/editing/set_night_mode": "/cv/projects/editing"
}

ENDPOINT_POST_FUNCTIONS = {
      "/hello/save": "write_user_data",
      "/hello/set_night_mode": "set_night_mode",
      "/goodbye/set_night_mode": "set_night_mode",
      "/cv/set_night_mode": "set_night_mode",
      "/cv/job/set_night_mode": "set_night_mode",
      "/cv/education/set_night_mode": "set_night_mode",
      "/cv/skills/set_night_mode": "set_night_mode",
      "/cv/projects/set_night_mode": "set_night_mode",
      "/statistics/set_night_mode": "set_night_mode",
      "/cv/projects/editing/add": "add_project",
      "/cv/projects/editing/edit": "edit_project",
      "/cv/projects/editing/delete": "remove_project",
      "/cv/projects/editing/set_night_mode": "set_night_mode"
}