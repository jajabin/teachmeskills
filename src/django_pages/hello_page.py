import uuid
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect

import src.django_common.errors as errors
import src.django_common.instances as instances
import src.django_common.paths as paths
import src.django_common.responds as responds
import src.django_pages.statistics_page as stats
import src.django_utils.cookies_utils as cu
import src.django_utils.file_utils as fu
import src.django_utils.json_utils as ju
import src.django_utils.user_utils as uu
from src.django_common.night_mode import set_night_mode

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt    # what is it ????
def get_page_hello(request) -> HttpResponse:
    print(f"request = {request}")
    print(f"request.POST = {request.POST.get}")
    print(f"request.body = {request.body}")
    switcher = {
        "GET": show_page_hello,
        "POST": save_user_data,
    }
    if request.method in switcher:
        return switcher[request.method](request)
    else:
        raise errors.MethodNotAllowed


def show_page_hello(request) -> HttpResponse:
    stats.increment_page_visit(request.path)
    user_id = uu.get_user_id(request)
    user_session = uu.read_user_session(user_id)
    msg = fu.get_file_contents(paths.HELLO_HTML).format(formaction="/hello/set_night_mode", **user_session[user_id])
    msg = fu.get_file_contents(paths.TEMPLATE_HTML).format(title="Hello", **user_session[user_id], body=msg)

    return HttpResponse(msg)


def save_user_data(request) -> HttpResponse:
    redirect_to = instances.ENDPOINT_REDIRECTS[request.path]
    switcher = {
        "/hello/save": write_user_data,
        "/hello/set_night_mode": set_night_mode,
    }
    if request.path in switcher:
        return switcher[request.path](request, redirect_to)
    else:
        raise errors.MethodNotAllowed


def write_user_data(request, redirect_to) -> HttpResponse:
    user_data = ju.read_json_file(paths.USER_SESSIONS)
    new_user = instances.NEW_USER
    new_user[instances.NAME_key] = request.POST.get(instances.NAME_key, "Dude")
    new_user[instances.AGE_key] = request.POST.get(instances.AGE_key, "")

    if new_user[instances.AGE_key]:
        today = datetime.today().year
        age = int(new_user[instances.AGE_key])
        new_user[instances.YEAR_key] = str(today - age)

    user_id = str(uuid.uuid1())
    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id].update(new_user)

    ju.update_json_file(user_data, paths.USER_SESSIONS)
    #cookie_master = cu.set_cookies(server_inst, {instances.USER_ID: user_id})

    return HttpResponseRedirect(redirect_to)         #set cookies
