from datetime import datetime, timedelta

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import common.errors as errors
import common.paths as paths
import common.responds as responds
import utils.json_utils as ju
import utils.user_utils as uu
import common.instances as instances
from common.night_mode import set_night_mode


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


@require_http_methods(["GET", "POST"])
@csrf_exempt
def get_page_statistics(request) -> HttpResponse:
    switcher = {
        "GET": show_page_statistics,
        "POST": save_page_statistics,
    }

    return switcher[request.method](request)


def show_page_statistics(request) -> HttpResponse:
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

    return responds.respond_200(request, paths.STATISTICS_HTML, {"action_night_mode": "/statistics/set_night_mode/",
                                                                 "stats": stats,
                                                                 **user_session[user_id]})


def save_page_statistics(request) -> HttpResponse:
    redirect_to = instances.ENDPOINT_REDIRECTS[request.path]
    switcher = {
        "/statistics/set_night_mode/": set_night_mode,
    }
    if request.path in switcher:
        return switcher[request.path](request, redirect_to)
    else:
        raise errors.PageNotFoundError
