BCKG_COLOR = "background_color"
TXT_COLOR = "text_color"

PROJECT_ID = "project_id"
USER_ID = "user_id"

AGE_key = "age"
YEAR_key = "year"

DARK_COLOR = "gray"
LIGHT_COLOR = "white"

COOKIE_TERM = 30

NEW_USER = {"name": "Dude", "age": "", "year": "", BCKG_COLOR: LIGHT_COLOR, TXT_COLOR: DARK_COLOR}
NEW_PROJECT = {"project_name": "", "project_date": "", "project_description": ""}

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
      "/hello/save": "/hello/",
      "/hello/set_night_mode": "/hello/set_night_mode",
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
      "/cv/projects/editing": "cv/projects/editing",
      "/cv/projects/editing/add": "cv/projects/editing",
      "/cv/projects/editing/edit": "cv/projects/editing",
      "/cv/projects/editing/delete": "cv/projects/editing",
      "/cv/projects/editing/set_night_mode": "cv/projects/editing"
}