from django.conf import settings

# ROOT_DIR = Path(__file__).parent.parent.parent.resolve()  # full path to dir where file is located
ROOT_DIR = settings.REPO_DIR

ENDPOINTS_SET = ROOT_DIR / "src/endpoint_functions.json"

USER_SESSIONS = ROOT_DIR / "sessions.json"
VISIT_COUNTERS = ROOT_DIR / "visit_counters.json"

CSS_STYLE = ROOT_DIR / "src/project/templates/css_style.css"

INDEX_HTML = ROOT_DIR / "src/project/templates/index.html"
HELLO_HTML = ROOT_DIR / "src/applications/hello/templates/hello/hello.html"
GOODBYE_HTML = ROOT_DIR / "src/applications/goodbye/templates/goodbye/goodbye.html"
STATISTICS_HTML = ROOT_DIR / "src/applications/stats/templates/stats/stats.html"
CV_HTML = ROOT_DIR / "src/applications/cv/templates/cv/cv.html"
CV_EDUCATION_HTML = ROOT_DIR / "src/applications/cv/templates/cv/cv_education.html"
CV_JOB_HTML = ROOT_DIR / "src/applications/cv/templates/cv/cv_job.html"
CV_SKILLS_HTML = ROOT_DIR / "src/applications/cv/templates/cv/cv_skills.html"
CV_PROJECTS_HTML = ROOT_DIR / "src/applications/cv/templates/cv/cv_projects.html"
CV_PROJECTS_ADDITING_HTML = ROOT_DIR / "src/applications/cv/templates/cv/cv_projects_additing.html"
CV_LINKS_HTML = ROOT_DIR / "src/applications/cv/templates/cv/cv_links.html"
CV_PROJECT_HTML = ROOT_DIR / "src/applications/cv/templates/cv/cv_project.html"
CV_PROJECT_EDITING_HTML = ROOT_DIR / "src/applications/cv/templates/cv/cv_project_editing.html"

CV_JSON = ROOT_DIR / "contents/cv_resume.json"
CV_EDUCATION_JSON = ROOT_DIR / "contents/cv_education.json"
CV_JOB_JSON = ROOT_DIR / "contents/cv_job.json"
CV_SKILLS_JSON = ROOT_DIR / "contents/cv_skills.json"
CV_PROJECTS_JSON = ROOT_DIR / "contents/cv_projects.json"
