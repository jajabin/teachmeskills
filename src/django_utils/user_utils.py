import logging
import uuid
from datetime import datetime
from typing import Dict
from urllib.parse import parse_qs

import src.django_common.instances as instances
import src.django_common.paths as paths
import src.django_utils.cookies_utils as cu
import src.django_utils.json_utils as ju


def get_user_id(request) -> str:
    #cookies_content = cu.get_cookies()
    cookies_content = request.COOKIES
    print(f"cookies = {cookies_content}")
    logging.debug(f"cookies content = {cookies_content}")

    return cookies_content[instances.USER_ID] if instances.USER_ID in cookies_content else str(uuid.uuid4())


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