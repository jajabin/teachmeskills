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
from django.urls import path, re_path
import logging

from requests import models

from src.pages.cv_page import handler_page_cv
from src.pages.goodbye_page import get_page_goodbye
from src.pages.hello_page import get_page_hello
from src.styles.css_style import get_cv_style
from src.pages.statistics_page import get_page_statistics


logging.basicConfig(level=logging.DEBUG)


# optimize endpoints !!!
urlpatterns = [
    # re_path(r"cv\/project/(.+)\/", handler_page_cv),
    # re_path(r"cv\/project(/(?P<project_id>.+))$", handler_page_cv),
    re_path(r"cv/project/(?P<project_id>\w+)/", handler_page_cv),
    path('hello/', get_page_hello),
    re_path(r"hello/\w+", get_page_hello),
    path('goodbye/', get_page_goodbye),
    re_path(r"goodbye/\w+", get_page_goodbye),
    path('statistics/', get_page_statistics),
    re_path(r"statistics/\w+", get_page_statistics),
    path('cv/projects/editing/', handler_page_cv),
    re_path(r"cv/projects/editing/\w+", handler_page_cv),
    path('cv/', handler_page_cv),
    path('cv/<str:module>/', handler_page_cv),
    path('cv/<str:module>/<str:operation>/', handler_page_cv),
    path('admin/', admin.site.urls),
    path('cv_style.css', get_cv_style),
    # path('hello/', get_page_hello),
    # path('hello/save', get_page_hello),
    # path('hello/set_night_mode', get_page_hello),
    # path('goodbye/', get_page_goodbye),
    # path('goodbye/set_night_mode', get_page_goodbye),
    # path('statistics/', get_page_statistics),
    # path('statistics/set_night_mode', get_page_statistics),
    # path('cv/', handler_page_cv),
    # path('cv/set_night_mode', handler_page_cv),
    # path('cv/job/', handler_page_cv),
    # path('cv/job/set_night_mode', handler_page_cv),
    # path('cv/skills/', handler_page_cv),
    # path('cv/skills/set_night_mode', handler_page_cv),
    # path('cv/education/', handler_page_cv),
    # path('cv/education/set_night_mode', handler_page_cv),
    # path('cv/projects/', handler_page_cv),
    # path('cv/projects/set_night_mode', handler_page_cv),
    # path('cv/projects/editing/', handler_page_cv),
    # path('cv/projects/editing/set_night_mode', handler_page_cv),
    # path('cv/projects/editing/add', handler_page_cv),
    # path('cv/projects/editing/edit', handler_page_cv),
    # path('cv/projects/editing/delete', handler_page_cv),
    # path('cv/project/', handler_page_cv),
    # path('cv/project/<str:project_id>/', handler_page_cv),
    # path('cv/project/<str:project_id>/set_night_mode', handler_page_cv),
]