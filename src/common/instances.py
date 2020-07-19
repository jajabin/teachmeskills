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

PROJECT_ID_key = "id"
PROJECT_NAME_key = "name"
PROJECT_DATE_key = "date"
PROJECT_DESCRIPTION_key = "description"

NEW_USER = {NAME_key: "Dude", AGE_key: "", YEAR_key: "", BCKG_COLOR: LIGHT_COLOR, TXT_COLOR: DARK_COLOR}
NEW_PROJECT = {PROJECT_NAME_key: "", PROJECT_DATE_key: "", PROJECT_DESCRIPTION_key: ""}

ENDPOINT_REDIRECTS = {
    "/hello": "/hello",
    "/hello/save": "/hello",
    "/hello/set_night_mode/": "/hello",
    "/goodbye": "/goodbye",
    "/goodbye/set_night_mode/": "/goodbye",
    "/cv": "/cv",
    "/cv/set_night_mode/": "/cv",
    "/cv/job": "/cv/job",
    "/cv/job/set_night_mode/": "/cv/job",
    "/cv/education": "/cv/education",
    "/cv/education/set_night_mode/": "/cv/education",
    "/cv/skills": "/cv/skills",
    "/cv/skills/set_night_mode/": "/cv/skills",
    "/cv/projects": "/cv/projects",
    "/cv/projects/set_night_mode/": "/cv/projects",
    "/stats": "/stats",
    "/stats/set_night_mode/": "/stats",
    "/cv/projects/additing": "/cv/projects/additing",
    "/cv/projects/additing/add": "/cv/projects",
    "/cv/projects/additing/set_night_mode/": "/cv/projects/additing"
}
