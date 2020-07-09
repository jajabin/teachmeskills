from datetime import datetime

from django.http import HttpResponse

import src.common.errors as errors
import src.common.instances as instances
import src.common.paths as paths
import src.common.responds as responds
import src.pages.statistics_page as stats
import src.utils.file_utils as fu
import src.utils.user_utils as uu
from src.common.night_mode import set_night_mode
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_page_goodbye(request) -> HttpResponse:
    switcher = {
        "GET": show_page_goodbye,
        "POST": save_page_goodbye,
    }
    if request.method in switcher:
        return switcher[request.method](request)
    else:
        raise errors.MethodNotAllowed


def show_page_goodbye(request) -> HttpResponse:
    stats.increment_page_visit(request.path)
    today = datetime.today()
    phrase = say_bye(today.hour)

    user_id = uu.get_user_id(request)
    user_session = uu.read_user_session(user_id)

    msg = fu.get_file_contents(paths.GOODBYE_HTML).format(date=today, phrase=phrase, **user_session[user_id])
    msg = fu.get_file_contents(paths.TEMPLATE_HTML).format(title="Goodbye", **user_session[user_id], body=msg)

    return responds.respond_200(msg)


def save_page_goodbye(request) -> HttpResponse:
    redirect_to = instances.ENDPOINT_REDIRECTS[request.path]
    switcher = {
      "/goodbye/set_night_mode": set_night_mode,
    }
    if request.path in switcher:
        return switcher[request.path](request, redirect_to)
    else:
        raise errors.MethodNotAllowed


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
