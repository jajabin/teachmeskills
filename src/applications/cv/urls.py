from django.urls import path

from applications.cv.apps import CVConfig
from applications.cv.views import NightModeView, CVView, JobView, SkillsView, EducationView, ProjectsView, \
    AddProjectView, SingleProjectView, EditProjectView

app_name = CVConfig.label

urlpatterns = [
    path('', CVView.as_view(), name='root'),
    path('set_night_mode/', NightModeView.as_view()),
    path('job/', JobView.as_view(), name='job'),
    path('job/set_night_mode/', NightModeView.as_view()),
    path('skills/', SkillsView.as_view(), name='skills'),
    path('skills/set_night_mode/', NightModeView.as_view()),
    path('education/', EducationView.as_view(), name='education'),
    path('education/set_night_mode/', NightModeView.as_view()),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('projects/set_night_mode/', NightModeView.as_view()),
    path('projects/additing/', AddProjectView.as_view()),
    path('projects/additing/set_night_mode/', NightModeView.as_view()),
    path('projects/additing/add', AddProjectView.as_view()),
    path('project/<str:project_id>/', SingleProjectView.as_view(), name='single_project'),
    path('project/<str:project_id>/set_night_mode/', NightModeView.as_view()),
    path('project/<str:project_id>/delete', SingleProjectView.as_view()),
    path('project/<str:project_id>/editing', EditProjectView.as_view()),
    path('project/<str:project_id>/editing/edit', EditProjectView.as_view()),
]
