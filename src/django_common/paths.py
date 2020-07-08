from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.parent.resolve()  # full path to dir where file is located

ENDPOINTS_SET = PROJECT_DIR / "src/endpoint_functions.json"

USER_SESSIONS = PROJECT_DIR / "sessions.json"
VISIT_COUNTERS = PROJECT_DIR / "visit_counters.json"

CV_STYLE = PROJECT_DIR / "pages/cv_style.css"

TEMPLATE_HTML = PROJECT_DIR / "pages/template.html"
HELLO_HTML = PROJECT_DIR / "pages/hello.html"
GOODBYE_HTML = PROJECT_DIR / "pages/goodbye.html"
STATISTICS_HTML = PROJECT_DIR / "pages/statistics.html"
CV_HTML = PROJECT_DIR / "pages/cv.html"
CV_EDUCATION_HTML = PROJECT_DIR / "pages/cv_education.html"
CV_JOB_HTML = PROJECT_DIR / "pages/cv_job.html"
CV_SKILLS_HTML = PROJECT_DIR / "pages/cv_skills.html"
CV_PROJECTS_HTML = PROJECT_DIR / "pages/cv_projects.html"
CV_PROJECTS_EDITING_HTML = PROJECT_DIR / "pages/cv_projects_editing.html"
CV_LINKS_HTML = PROJECT_DIR / "pages/cv_links.html"
CV_PROJECT_HTML = PROJECT_DIR / "pages/cv_project.html"

CV_JSON = PROJECT_DIR / "contents/cv_resume.json"
CV_EDUCATION_JSON = PROJECT_DIR / "contents/cv_education.json"
CV_JOB_JSON = PROJECT_DIR / "contents/cv_job.json"
CV_SKILLS_JSON = PROJECT_DIR / "contents/cv_skills.json"
CV_PROJECTS_JSON = PROJECT_DIR / "contents/cv_projects.json"
