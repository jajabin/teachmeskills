"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
import logging

from src.common import paths
from src.pages.cv_page import get_page_cv, get_page_cv_job, get_page_cv_skills, get_page_cv_education, \
    get_page_cv_projects, get_page_projects_editing, get_page_cv_project
from src.pages.goodbye_page import get_page_goodbye
from src.pages.hello_page import get_page_hello
from src.styles.css_style import get_cv_style
from src.pages.statistics_page import get_page_statistics
import src.utils.file_utils as fu


logging.basicConfig(level=logging.DEBUG)


def show_index(_request):
    msg = fu.get_file_contents(paths.INDEX_HTML)
    return HttpResponse(msg)


urlpatterns = [
    # re_path(r"cv\/project/(.+)\/", handler_page_cv),
    # re_path(r"cv\/project(/(?P<project_id>.+))$", handler_page_cv),
    # re_path(r"cv/project/(?P<project_id>\w+)/", handler_page_cv),
    # path('hello/', get_page_hello),
    # re_path(r"hello/\w+", get_page_hello),
    # path('goodbye/', get_page_goodbye),
    # re_path(r"goodbye/\w+", get_page_goodbye),
    # path('statistics/', get_page_statistics),
    # re_path(r"statistics/\w+", get_page_statistics),
    # path('cv/projects/editing/', handler_page_cv),
    # re_path(r"cv/projects/editing/\w+", handler_page_cv),
    # path('cv/', handler_page_cv),
    # path('cv/<str:module>/', handler_page_cv),
    # path('cv/<str:module>/<str:operation>/', handler_page_cv),
    path('admin/', admin.site.urls),
    path('cv_style.css', get_cv_style),
    path('', show_index),
    path('hello/', get_page_hello),
    path('hello/save', get_page_hello),
    path('hello/set_night_mode/', get_page_hello),
    path('goodbye/', get_page_goodbye),
    path('goodbye/set_night_mode/', get_page_goodbye),
    path('statistics/', get_page_statistics),
    path('statistics/set_night_mode/', get_page_statistics),
    path('cv/', get_page_cv),
    path('cv/set_night_mode/', get_page_cv),
    path('cv/job/', get_page_cv_job),
    path('cv/job/set_night_mode/', get_page_cv_job),
    path('cv/skills/', get_page_cv_skills),
    path('cv/skills/set_night_mode/', get_page_cv_skills),
    path('cv/education/', get_page_cv_education),
    path('cv/education/set_night_mode/', get_page_cv_education),
    path('cv/projects/', get_page_cv_projects),
    path('cv/projects/set_night_mode/', get_page_cv_projects),
    path('cv/projects/editing/', get_page_projects_editing),
    path('cv/projects/editing/set_night_mode/', get_page_projects_editing),
    path('cv/projects/editing/add', get_page_projects_editing),
    path('cv/projects/editing/edit', get_page_projects_editing),
    path('cv/projects/editing/delete', get_page_projects_editing),
    path('cv/project/', get_page_cv_project),
    path('cv/project/<str:project_id>/', get_page_cv_project),
    path('cv/project/<str:project_id>/set_night_mode/', get_page_cv_project),
    path('cv/project/<str:project_id>/delete', get_page_cv_project),
]
