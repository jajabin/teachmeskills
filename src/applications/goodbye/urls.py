from django.urls import path

from applications.goodbye.apps import GoodbyeConfig
from applications.goodbye.views import GoodbyeView, NightModeView

app_name = GoodbyeConfig.label

urlpatterns = [
    path("", GoodbyeView.as_view(), name='root'),
    path("set_night_mode/", NightModeView.as_view()),
]
