from src.server import *
from src.statistics_page import *


def get_page_goodbye(self, method: str, endpoint: str, _qs) -> None:
    switcher = {
        "GET": show_page_goodbye,
        "POST": save_page_goodbye,
    }
    if method in switcher:
        switcher[method](self, endpoint, "/goodbye")
    else:
        raise MethodNotAllowed


def show_page_goodbye(self, endpoint: str, _redirect_to) -> None:
    increment_page_visit(self, endpoint)
    today = datetime.today()
    phrase = say_bye(today.hour)

    user_id = get_user_id(self)
    user_session = read_user_session(self, user_id)

    msg = get_file_contents("pages/goodbye.html").format(date=today, phrase=phrase, **user_session[user_id])  # format ???
    respond_200(self, msg, "text/html")


def save_page_goodbye(self, endpoint: str, redirect_to: str):
    switcher = {
        "/goodbye/set_night_mode": set_night_mode,
    }
    if endpoint in switcher:
        switcher[endpoint](self, redirect_to)
    else:
        raise MethodNotAllowed


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

