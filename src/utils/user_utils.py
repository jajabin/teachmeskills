import logging
import uuid
from typing import Dict

import common.instances as instances
import common.paths as paths
import utils.json_utils as ju


def get_user_id(request) -> str:
    cookies_content = request.COOKIES.get(instances.USER_ID)
    logging.debug(f"cookies content = {cookies_content}")
    return cookies_content if cookies_content is not None else str(uuid.uuid4())


def read_user_session(user_id: str) -> Dict[str, str]:
    user_data = ju.read_json_file(paths.USER_SESSIONS)
    current_user = {user_id: instances.NEW_USER.copy()}
    if user_id in user_data:
        current_user[user_id].update(user_data[user_id])
    return current_user


def parse_received_data(request) -> Dict[str, str]:
    new_data = {}
    for key, value in request.POST.items():
        if value:
            new_data[key] = value
    return new_data
