from src.errors import *
from src.statistics_page import *

PROJECT_DIR = Path(__file__).parent.parent.resolve()
USER_SESSIONS = PROJECT_DIR / "sessions.json"


def get_page_hello(self, method: str, endpoint: str, qs: str) -> None:
    switcher = {
        "GET": show_page_hello,
        "POST": save_user_data,
    }
    if method in switcher:
        switcher[method](self, endpoint, USER_SESSIONS)
    else:
        raise MethodNotAllowed


def show_page_hello(self, endpoint: str, _content_file):
    increment_page_visit(self, endpoint)

    user_id = get_user_id(self)
    user_session = read_user_session(self, user_id)

    msg = get_file_contents("pages/hello.html").format(**user_session[user_id])

    #cookie_master = set_cookies(self, {"user_id": user_id})
    #respond_200(self, msg, "text/html", cookie_master)
    respond_200(self, msg, "text/html")


def save_user_data(self, endpoint: str, _content_file) -> None:
    switcher = {
        "/hello/set_night_mode": set_night_mode,
        "/hello/save": write_user_data,
    }
    if endpoint in switcher:
        switcher[endpoint](self, "/hello")
    else:
        raise MethodNotAllowed


def write_user_data(self, _endpoint):
    user_data = read_json_file(USER_SESSIONS)
    new_user_data = parse_user_sessions(self)

    if "name" not in new_user_data:
        raise MissingData

    user_id = str(uuid.uuid1())
    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id].update(new_user_data)
    today = datetime.today().year
    user_data[user_id]["year"] = today - int(user_data[user_id]["age"]) if "age" in new_user_data else "-"
    user_data[user_id]["background_color"] = "white"
    user_data[user_id]["text_color"] = "gray"

    update_json_file(user_data, USER_SESSIONS)
    cookie_master = set_cookies(self, {"user_id": user_id})

    respond_302(self, "/hello", cookie_master)
