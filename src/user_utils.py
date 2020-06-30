import uuid
from urllib.parse import parse_qs
from src.json_utils import *
from src.cookies_utils import *

PROJECT_DIR = Path(__file__).parent.parent.resolve()
USER_SESSIONS = PROJECT_DIR / "sessions.json"


def get_user_id(self) -> str:
    cookies_content = get_cookies(self)
    print(f"cookies content = {cookies_content}")
    try:
        return cookies_content["user_id"]
    except:
        return str(uuid.uuid1())


def read_user_session(self, user_id: str) -> Dict[str, str]:
    user_data = read_json_file(USER_SESSIONS)

    current_user_session = {}
    if user_id in user_data:
        current_user_session[user_id] = user_data[user_id]
        today = datetime.today().year
        current_user_session[user_id]["year"] = today - int(current_user_session[user_id]["age"]) if \
        current_user_session[user_id]["age"] != "-" else "-"
    else:
        current_user_session[user_id] = create_new_user_session()
        #user_data.update(current_user_session)
        #update_json_file(user_data, "sessions.json")

    return current_user_session


def create_new_user_session() -> Dict[str, str]:
    temp_user_data = {"name": "Dude", "age": "-", "year": "-", "background_color": "white", "text_color": "gray"}
    return temp_user_data


def parse_user_sessions(self) -> Dict[str, str]:
    content_length = int(self.headers["Content-Length"])
    data = self.rfile.read(content_length)
    payload = data.decode()
    qs = parse_qs(payload)
    user_data = {}
    for key, values in qs.items():
        if not values:
            continue
        user_data[key] = values[0]

    return user_data


