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

from src.django_pages.cv_page import handler_page_cv
from src.django_pages.goodbye_page import get_page_goodbye
from src.django_pages.hello_page import get_page_hello
from src.django_styles.css_style import get_cv_style
from src.django_pages.statistics_page import get_page_statistics


# optimize endpoints !!!
urlpatterns = [
    path('admin/', admin.site.urls),
    path('cv_style.css', get_cv_style),
    path('hello/', get_page_hello),
    path('hello/save', get_page_hello),
    path('hello/set_night_mode', get_page_hello),
    path('goodbye/', get_page_goodbye),
    path('goodbye/set_night_mode', get_page_goodbye),
    path('statistics/', get_page_statistics),
    path('statistics/set_night_mode', get_page_statistics),
    path('cv/', handler_page_cv),
    path('cv/set_night_mode', handler_page_cv),
    path('cv/job/', handler_page_cv),
    path('cv/job/set_night_mode', handler_page_cv),
    path('cv/skills/', handler_page_cv),
    path('cv/skills/set_night_mode', handler_page_cv),
    path('cv/education/', handler_page_cv),
    path('cv/education/set_night_mode', handler_page_cv),
    path('cv/projects/', handler_page_cv),
    path('cv/projects/set_night_mode', handler_page_cv),
    path('cv/projects/editing/', handler_page_cv),
    path('cv/projects/editing/set_night_mode', handler_page_cv),
    path('cv/projects/editing/add', handler_page_cv),
    path('cv/projects/editing/edit', handler_page_cv),
    path('cv/projects/editing/delete', handler_page_cv),
    path('cv/project/', handler_page_cv),
    path('cv/project/<str:project_id>/', handler_page_cv),
    path('cv/project/<str:project_id>/set_night_mode', handler_page_cv),
    #re_path(r"^/cv\/project\/<str:project_id>\/(\w+)", handler_page_cv),
]