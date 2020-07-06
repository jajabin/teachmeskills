import uuid
from datetime import datetime

import src.common.errors as errors
import src.common.instances as instances
import src.common.paths as paths
import src.common.responds as responds
import src.pages.statistics_page as stats
import src.utils.cookies_utils as cu
import src.utils.file_utils as fu
import src.utils.json_utils as ju
import src.utils.user_utils as uu
from src.common.night_mode import set_night_mode


def get_page_hello(server_inst, method: str, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_hello,
        "POST": save_user_data,
    }
    if method in switcher:
        switcher[method](server_inst, endpoint)
    else:
        raise errors.MethodNotAllowed


def show_page_hello(server_inst, endpoint: str):
    stats.increment_page_visit(endpoint)
    user_id = uu.get_user_id(server_inst)
    user_session = uu.read_user_session(user_id)
    msg = fu.get_file_contents(paths.HELLO_HTML).format(**user_session[user_id])

    # cookie_master = set_cookies(server_inst, {"user_id": user_id})
    # respond_200(server_inst, msg, "text/html", cookie_master)
    responds.respond_200(server_inst, msg, "text/html")


def save_user_data(server_inst, endpoint: str) -> None:
    redirect_to = instances.ENDPOINT_REDIRECTS[endpoint]
    switcher = {
        "/hello/save": write_user_data,
        "/hello/set_night_mode": set_night_mode,
    }
    if endpoint in switcher:
        switcher[endpoint](server_inst, redirect_to)
    else:
        raise errors.MethodNotAllowed


def write_user_data(server_inst, redirect_to):
    user_data = ju.read_json_file(paths.USER_SESSIONS)
    new_user = instances.NEW_USER
    new_user.update(uu.parse_received_data(server_inst))

    if new_user[instances.AGE_key]:
        today = datetime.today().year
        age = int(new_user[instances.AGE_key])
        new_user[instances.YEAR_key] = str(today - age)

    user_id = str(uuid.uuid1())
    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id].update(new_user)

    ju.update_json_file(user_data, paths.USER_SESSIONS)
    cookie_master = cu.set_cookies(server_inst, {instances.USER_ID: user_id})

    responds.respond_302(server_inst, redirect_to, cookie_master)
