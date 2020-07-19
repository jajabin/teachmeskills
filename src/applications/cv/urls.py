from django.urls import path

from applications.cv.apps import CVConfig
from applications.cv.views import get_page_cv, get_page_cv_education, get_page_cv_job, get_page_cv_skills, \
    get_page_cv_projects, get_page_projects_editing, get_page_cv_project, get_page_cv_project_editing

app_name = CVConfig.label

urlpatterns = [
    path('', get_page_cv),
    path('set_night_mode/', get_page_cv),
    path('job/', get_page_cv_job),
    path('job/set_night_mode/', get_page_cv_job),
    path('skills/', get_page_cv_skills),
    path('skills/set_night_mode/', get_page_cv_skills),
    path('education/', get_page_cv_education),
    path('education/set_night_mode/', get_page_cv_education),
    path('projects/', get_page_cv_projects),
    path('projects/set_night_mode/', get_page_cv_projects),
    path('projects/additing/', get_page_projects_editing),
    path('projects/additing/set_night_mode/', get_page_projects_editing),
    path('projects/additing/add', get_page_projects_editing),
    path('project/', get_page_cv_project),
    path('project/<str:project_id>/', get_page_cv_project, name='url_project'),
    path('project/<str:project_id>/set_night_mode/', get_page_cv_project),
    path('project/<str:project_id>/delete', get_page_cv_project),
    path('project/<str:project_id>/editing', get_page_cv_project_editing),
    path('project/<str:project_id>/editing/edit', get_page_cv_project_editing),
]
