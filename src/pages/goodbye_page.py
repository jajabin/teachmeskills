from datetime import datetime

import src.common.errors as errors
import src.common.instances as instances
import src.common.night_mode as nm
import src.common.paths as paths
import src.common.responds as responds
import src.pages.statistics_page as stats
import src.utils.file_utils as fu
import src.utils.user_utils as uu


def get_page_goodbye(server_inst, method: str, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_goodbye,
        "POST": save_page_goodbye,
    }
    if method in switcher:
        switcher[method](server_inst, endpoint)
    else:
        raise errors.MethodNotAllowed


def show_page_goodbye(server_inst, endpoint: str) -> None:
    stats.increment_page_visit(endpoint)
    today = datetime.today()
    phrase = say_bye(today.hour)

    user_id = uu.get_user_id(server_inst)
    user_session = uu.read_user_session(user_id)

    msg = fu.get_file_contents(paths.GOODBYE_HTML).format(date=today, phrase=phrase,
                                                          **user_session[user_id])  # format ???
    responds.respond_200(server_inst, msg, "text/html")


def get_redirect_to(endpoint: str) -> str:
    return instances.ENDPOINT_REDIRECTS[endpoint]


def save_page_goodbye(server_inst, endpoint: str):
    redirect_to = get_redirect_to(endpoint)
    switcher = {
        "/goodbye/set_night_mode": nm.set_night_mode,
    }
    if endpoint in switcher:
        switcher[endpoint](server_inst, redirect_to)
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
