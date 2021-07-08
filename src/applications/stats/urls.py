from django.urls import path

from applications.stats.apps import StatsConfig
from applications.stats.views import StatsView, NightModeView

app_name = StatsConfig.label

urlpatterns = [
    path("", StatsView.as_view(), name='root'),
    path("set_night_mode/", NightModeView.as_view(), name="index"),
]
