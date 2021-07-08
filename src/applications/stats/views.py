from django.http import HttpResponse

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView

from applications.stats.models import StatsModel
from project.utils.night_mode import set_night_mode, get_theme
from project.utils import paths as paths, instances as instances


class StatsView(TemplateView):
    template_name = paths.STATISTICS_HTML

    def get(self, request) -> HttpResponse:
        stats = StatsModel.get_stats()
        theme = get_theme(self.request)
        context = {"stats": stats, **theme}
        return render(request, paths.STATISTICS_HTML, context)


class NightModeView(View):
    @csrf_exempt
    def post(self, request):
        return set_night_mode(request, instances.ENDPOINT_REDIRECTS[request.path])
