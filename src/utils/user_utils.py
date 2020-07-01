import logging
import uuid
from datetime import datetime
from typing import Dict
from urllib.parse import parse_qs

import src.common.instances as instances
import src.common.paths as paths
import src.utils.cookies_utils as cu
import src.utils.json_utils as ju


def get_user_id(self) -> str:
    cookies_content = cu.get_cookies(self)
    logging.info(f"cookies content = {cookies_content}")

    return cookies_content["user_id"] if "user_id" in cookies_content else str(uuid.uuid1())


def read_user_session(user_id: str) -> Dict[str, str]:
    user_data = ju.read_json_file(paths.USER_SESSIONS)

    current_user = {}
    if user_id in user_data:
        current_user[user_id] = user_data[user_id]
        if current_user[user_id]["age"]:
            today = datetime.today().year
            age = int(current_user[user_id]["age"])
            current_user[user_id]["year"] = str(today - age)
    else:
        current_user[user_id] = create_new_user_session()
        # user_data.update(current_user_session)
        # update_json_file(user_data, paths.USER_SESSIONS)

    return current_user


def create_new_user_session() -> Dict[str, str]:
    return instances.NEW_USER


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
