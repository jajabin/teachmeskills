from datetime import datetime, timedelta

from django.http import HttpResponse

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView

from project.utils.night_mode import set_night_mode, get_theme
from project.utils import user_utils as uu, json_utils as ju, paths as paths, instances as instances


def increment_page_visit(endpoint: str) -> None:
    today = str(datetime.today().date())
    statistics_content = ju.read_json_file(paths.VISIT_COUNTERS)

    if endpoint not in statistics_content:
        statistics_content[endpoint] = {}
    if today not in statistics_content[endpoint]:
        statistics_content[endpoint][today] = 0

    statistics_content[endpoint][today] += 1
    ju.write_json_file(paths.VISIT_COUNTERS, statistics_content)


def calculate_stats(page_statistics, start_date, count_days) -> int:
    visit_counter = 0
    for day_counter in range(0, count_days + 1):
        day = str(start_date - timedelta(days=day_counter))
        if day in page_statistics:
            visit_counter += page_statistics[day]

    return visit_counter


class StatsView(TemplateView):
    template_name = paths.STATISTICS_HTML

    def get(self, request) -> HttpResponse:
        statistics_content = ju.read_json_file(paths.VISIT_COUNTERS)

        today = datetime.today().date()
        stats = []
        for page in statistics_content:
            stat = {"page": page,
                    "today": calculate_stats(statistics_content[page], today, 0),
                    "yesterday": calculate_stats(statistics_content[page], today - timedelta(days=1), 0),
                    "week": calculate_stats(statistics_content[page], today, 7),
                    "month": calculate_stats(statistics_content[page], today, 30)}
            stats.append(stat)

        user_id = uu.get_user_id(request)
        user_session = uu.read_user_session(user_id)
        theme = get_theme(self.request)
        context = {"stats": stats, **theme}

        return render(request, paths.STATISTICS_HTML, context)


class NightModeView(View):
    @csrf_exempt
    def post(self, request):
        return set_night_mode(request, instances.ENDPOINT_REDIRECTS[request.path])
