import uuid
from datetime import datetime
from typing import Dict
from urllib.parse import parse_qs

import src.common.instances as instances
import src.common.paths as paths
import src.utils.cookies_utils as cu
import src.utils.json_utils as ju


def get_user_id(server_inst) -> str:
    cookies_content = cu.get_cookies(server_inst)
    print(f"cookies content = {cookies_content}")

    return cookies_content[instances.USER_ID] if instances.USER_ID in cookies_content else str(uuid.uuid1())


def read_user_session(user_id: str) -> Dict[str, str]:
    user_data = ju.read_json_file(paths.USER_SESSIONS)

    current_user = {}
    if user_id in user_data:
        current_user[user_id] = user_data[user_id]
        if current_user[user_id][instances.AGE_key]:
            today = datetime.today().year
            age = int(current_user[user_id][instances.AGE_key])
            current_user[user_id][instances.YEAR_key] = str(today - age)
    else:
        current_user[user_id] = create_new_user_session()
        # user_data.update(current_user_session)
        # update_json_file(user_data, paths.USER_SESSIONS)

    return current_user


def create_new_user_session() -> Dict[str, str]:
    return instances.NEW_USER


def parse_received_data(server_inst) -> Dict[str, str]:
    content_length = int(server_inst.headers["Content-Length"])
    data = server_inst.rfile.read(content_length)
    payload = data.decode()
    qs = parse_qs(payload)
    user_data = {}
    for key, values in qs.items():
        if not values:
            continue
        user_data[key] = values[0]

    return user_data
