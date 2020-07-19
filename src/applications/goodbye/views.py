from datetime import datetime

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from applications.stats.views import increment_page_visit
from common import responds as responds, paths as paths, instances as instances, errors as errors
from common.night_mode import set_night_mode
from utils import user_utils as uu


@require_http_methods(["GET", "POST"])
@csrf_exempt
def get_page_goodbye(request) -> HttpResponse:
    switcher = {
        "GET": show_page_goodbye,
        "POST": save_page_goodbye,
    }

    return switcher[request.method](request)


def show_page_goodbye(request) -> HttpResponse:
    increment_page_visit(request.path)
    today = datetime.today()
    phrase = say_bye(today.hour)

    user_id = uu.get_user_id(request)
    user_session = uu.read_user_session(user_id)

    return responds.respond_200(request, paths.GOODBYE_HTML, {"action_night_mode": "/goodbye/set_night_mode/",
                                                              "date": today,
                                                              "phrase": phrase,
                                                              **user_session[user_id]})


def save_page_goodbye(request) -> HttpResponse:
    redirect_to = instances.ENDPOINT_REDIRECTS[request.path]
    switcher = {
      "/goodbye/set_night_mode/": set_night_mode,
    }
    if request.path in switcher:
        return switcher[request.path](request, redirect_to)
    else:
        raise errors.PageNotFoundError


def say_bye(hour) -> str:
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