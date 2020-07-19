from django.urls import path

from applications.goodbye.views import get_page_goodbye

urlpatterns = [
    path("", get_page_goodbye),
    path("set_night_mode/", get_page_goodbye),
]
