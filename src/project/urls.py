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
from django.urls import path, include
import logging

from django.views.generic import TemplateView

from project.utils import paths

logging.basicConfig(level=logging.DEBUG)


urlpatterns = [
    # re_path(r"cv\/project/(.+)\/", handler_page_cv),
    # re_path(r"cv\/project(/(?P<project_id>.+))$", handler_page_cv),
    # re_path(r"cv/project/(?P<project_id>\w+)/", handler_page_cv),
    # path('hello/', get_page_hello),
    # re_path(r"hello/\w+", get_page_hello),
    # path('goodbye/', get_page_goodbye),
    # re_path(r"goodbye/\w+", get_page_goodbye),
    # path('stats/', get_page_statistics),
    # re_path(r"stats/\w+", get_page_statistics),
    # path('cv/projects/editing/', handler_page_cv),
    # re_path(r"cv/projects/editing/\w+", handler_page_cv),
    # path('cv/', handler_page_cv),
    # path('cv/<str:module>/', handler_page_cv),
    # path('cv/<str:module>/<str:operation>/', handler_page_cv),
    path('admin/', admin.site.urls),
    path('css_style.css', TemplateView.as_view(template_name=paths.CSS_STYLE, content_type="text/css")),
    path('', TemplateView.as_view(template_name=paths.INDEX_HTML)),
    path('hello/', include("applications.hello.urls")),
    path('goodbye/', include("applications.goodbye.urls")),
    path('stats/', include("applications.stats.urls")),
    path('cv/', include("applications.cv.urls")),
]
