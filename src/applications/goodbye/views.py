from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View


from project.utils.night_mode import set_night_mode, get_theme
from project.utils import paths as paths, instances as instances
from project.utils.stats_utils import increment_page_visit, increment_visit


@increment_visit
class GoodbyeView(TemplateView):
    template_name = paths.GOODBYE_HTML

    def get(self, request) -> HttpResponse:
        #increment_page_visit(request.path)

        today = datetime.today()
        phrase = self.say_bye(today.hour)

        theme = get_theme(self.request)
        context = {"date": today, "phrase": phrase, **theme}

        return render(self.request, paths.GOODBYE_HTML, context)

    def say_bye(self, hour) -> str:
        if hour < 0:
            return "Invalid value."
        elif hour < 6 or hour == 23:
            return "Goodnight!"
        elif hour < 12:
            return "Good Morning!"
        elif hour < 18:
            return "Have a nice day!"
        elif hour < 23:
            return "Good Evening!"
        else:
            return "Invalid value."


class NightModeView(View):
    @csrf_exempt
    def post(self, request):
        return set_night_mode(request, instances.ENDPOINT_REDIRECTS[request.path])