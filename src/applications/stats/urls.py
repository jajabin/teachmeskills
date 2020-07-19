from django.urls import path

from applications.stats.views import get_page_statistics

urlpatterns = [
    path("", get_page_statistics),
    path("set_night_mode/", get_page_statistics),
]
