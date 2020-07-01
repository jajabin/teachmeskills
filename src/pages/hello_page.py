import uuid
from datetime import datetime

import src.common.errors as errors
import src.common.instances as instances
import src.common.night_mode as nm
import src.common.paths as paths
import src.common.responds as responds
import src.pages.statistics_page as stats
import src.utils.cookies_utils as cu
import src.utils.file_utils as fu
import src.utils.json_utils as ju
import src.utils.user_utils as uu


def get_page_hello(self, method: str, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_hello,
        "POST": save_user_data,
    }
    if method in switcher:
        switcher[method](self, endpoint, paths.USER_SESSIONS)
    else:
        raise errors.MethodNotAllowed


def show_page_hello(self, endpoint: str, _content_file):
    stats.increment_page_visit(endpoint)
    user_id = uu.get_user_id(self)
    user_session = uu.read_user_session(user_id)
    msg = fu.get_file_contents(paths.HELLO_HTML).format(**user_session[user_id])

    # cookie_master = set_cookies(self, {"user_id": user_id})
    # respond_200(self, msg, "text/html", cookie_master)
    responds.respond_200(self, msg, "text/html")


def save_user_data(self, endpoint: str, _content_file) -> None:
    switcher = {
        "/hello/set_night_mode": nm.set_night_mode,
        "/hello/save": write_user_data,
    }
    if endpoint in switcher:
        switcher[endpoint](self, "/hello")
    else:
        raise errors.MethodNotAllowed


def write_user_data(self, _endpoint):
    user_data = ju.read_json_file(paths.USER_SESSIONS)
    new_user = instances.NEW_USER
    new_user.update(uu.parse_user_sessions(self))

    if new_user["age"]:
        today = datetime.today().year
        age = int(new_user["age"])
        new_user["year"] = str(today - age)

    user_id = str(uuid.uuid1())
    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id].update(new_user)

    ju.update_json_file(user_data, paths.USER_SESSIONS)
    cookie_master = cu.set_cookies(self, {"user_id": user_id})

    responds.respond_302(self, "/hello", cookie_master)