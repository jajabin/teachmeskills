from django.urls import path

from applications.hello.apps import HelloConfig
from applications.hello.views import get_page_hello

app_name = HelloConfig.label

urlpatterns = [
    path("", get_page_hello, name='url_name'),
    path("save", get_page_hello),
    path("set_night_mode/", get_page_hello),
]
