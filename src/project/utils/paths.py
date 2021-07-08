from django.conf import settings

# ROOT_DIR = Path(__file__).parent.parent.parent.resolve()  # full path to dir where file is located
ROOT_DIR = settings.REPO_DIR
SOURCE_DIR = settings.BASE_DIR
APP_DIR = SOURCE_DIR / "applications"

USER_SESSIONS = ROOT_DIR / "sessions.json"
VISIT_COUNTERS = ROOT_DIR / "visit_counters.json"

CSS_STYLE = SOURCE_DIR / "project/templates/css_style.css"

INDEX_HTML = SOURCE_DIR / "project/templates/index.html"
HELLO_HTML = APP_DIR / "hello/templates/hello/hello.html"
GOODBYE_HTML = APP_DIR / "goodbye/templates/goodbye/goodbye.html"
STATISTICS_HTML = APP_DIR / "stats/templates/stats/stats.html"
CV_HTML = APP_DIR / "cv/templates/cv/cv.html"
CV_EDUCATION_HTML = APP_DIR / "cv/templates/cv/cv_education.html"
CV_JOB_HTML = APP_DIR / "cv/templates/cv/cv_job.html"
CV_SKILLS_HTML = APP_DIR / "cv/templates/cv/cv_skills.html"
CV_PROJECTS_HTML = APP_DIR / "cv/templates/cv/cv_projects.html"
CV_PROJECTS_ADDITING_HTML = APP_DIR / "cv/templates/cv/cv_projects_additing.html"
CV_LINKS_HTML = APP_DIR / "cv/templates/cv/cv_links.html"
CV_PROJECT_HTML = APP_DIR / "cv/templates/cv/cv_project.html"
CV_PROJECT_EDITING_HTML = APP_DIR / "cv/templates/cv/cv_project_editing.html"

CV_JSON = APP_DIR / "cv/contents/cv_resume.json"
CV_EDUCATION_JSON = APP_DIR / "cv/contents/cv_education.json"
CV_JOB_JSON = APP_DIR / "cv/contents/cv_job.json"
CV_SKILLS_JSON = APP_DIR / "cv/contents/cv_skills.json"
CV_PROJECTS_JSON = APP_DIR / "cv/contents/cv_projects.json"
