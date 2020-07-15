import logging
import uuid
from datetime import datetime

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

import common.errors as errors
import common.instances as instances
import common.paths as paths
import common.responds as responds
import pages.statistics_page as stats
import utils.json_utils as ju
import utils.user_utils as uu
from common.night_mode import set_night_mode

from django.views.decorators.csrf import csrf_exempt


@require_http_methods(["GET", "POST"])
@csrf_exempt    # what is it ????
def get_page_hello(request) -> HttpResponse:
    logging.debug(f"request = {request}")
    logging.debug(f"request.POST = {request.POST.get}")
    logging.debug(f"request.body = {request.body}")

    switcher = {
        "GET": show_page_hello,
        "POST": save_user_data,
    }

    return switcher[request.method](request)


def show_page_hello(request) -> HttpResponse:
    stats.increment_page_visit(request.path)
    user_id = uu.get_user_id(request)
    user_session = uu.read_user_session(user_id)

    return responds.respond_200(request, paths.HELLO_HTML, {"action_night_mode": "/hello/set_night_mode/",
                                                            **user_session[user_id]})


def save_user_data(request) -> HttpResponse:
    redirect_to = instances.ENDPOINT_REDIRECTS[request.path]
    switcher = {
        "/hello/save": write_user_data,
        "/hello/set_night_mode/": set_night_mode,
    }
    if request.path in switcher:
        return switcher[request.path](request, redirect_to)
    else:
        raise errors.PageNotFoundError


def write_user_data(request, redirect_to) -> HttpResponse:
    user_data = ju.read_json_file(paths.USER_SESSIONS)
    new_user = instances.NEW_USER.copy()
    new_user.update(uu.parse_received_data(request))

    if new_user[instances.AGE_key]:
        today = datetime.today().year
        age = int(new_user[instances.AGE_key])
        new_user[instances.YEAR_key] = str(today - age)

    user_id = str(uuid.uuid1())
    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id].update(new_user)
    ju.update_json_file(user_data, paths.USER_SESSIONS)

    return responds.respond_302(redirect_to, user_id)
