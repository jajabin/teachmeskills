# from pathlib import Path
from django.conf import settings

# ROOT_DIR = Path(__file__).parent.parent.parent.resolve()  # full path to dir where file is located
ROOT_DIR = settings.REPO_DIR

ENDPOINTS_SET = ROOT_DIR / "src/endpoint_functions.json"

USER_SESSIONS = ROOT_DIR / "sessions.json"
VISIT_COUNTERS = ROOT_DIR / "visit_counters.json"

CV_STYLE = ROOT_DIR / "pages/cv_style.css"

INDEX_HTML = ROOT_DIR / "index.html"
TEMPLATE_HTML = ROOT_DIR / "pages/template.html"
HELLO_HTML = ROOT_DIR / "pages/hello.html"
GOODBYE_HTML = ROOT_DIR / "pages/goodbye.html"
STATISTICS_HTML = ROOT_DIR / "pages/statistics.html"
CV_HTML = ROOT_DIR / "pages/cv.html"
CV_EDUCATION_HTML = ROOT_DIR / "pages/cv_education.html"
CV_JOB_HTML = ROOT_DIR / "pages/cv_job.html"
CV_SKILLS_HTML = ROOT_DIR / "pages/cv_skills.html"
CV_PROJECTS_HTML = ROOT_DIR / "pages/cv_projects.html"
CV_PROJECTS_EDITING_HTML = ROOT_DIR / "pages/cv_projects_editing.html"
CV_LINKS_HTML = ROOT_DIR / "pages/cv_links.html"
CV_PROJECT_HTML = ROOT_DIR / "pages/cv_project.html"

CV_JSON = ROOT_DIR / "contents/cv_resume.json"
CV_EDUCATION_JSON = ROOT_DIR / "contents/cv_education.json"
CV_JOB_JSON = ROOT_DIR / "contents/cv_job.json"
CV_SKILLS_JSON = ROOT_DIR / "contents/cv_skills.json"
CV_PROJECTS_JSON = ROOT_DIR / "contents/cv_projects.json"
