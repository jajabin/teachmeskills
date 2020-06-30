from src.user_utils import *
from src.responds import *

PROJECT_DIR = Path(__file__).parent.parent.resolve()
USER_SESSIONS = PROJECT_DIR / "sessions.json"


def set_night_mode(self, endpoint: str, _file_content=""):
    user_id = get_user_id(self)
    user_session = read_user_session(self, user_id)
    user_session[user_id]["background_color"], user_session[user_id]["text_color"] = \
                                        user_session[user_id]["text_color"], user_session[user_id]["background_color"]
    update_json_file(user_session, USER_SESSIONS)
    cookie_master = set_cookies(self, {"user_id": user_id})
    respond_302(self, endpoint, cookie_master)
