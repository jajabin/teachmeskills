import logging
import uuid
from datetime import datetime
from typing import Dict

import project.utils.instances as instances
import project.utils.paths as paths
import project.utils.json_utils as ju
from applications.hello.models import HelloModel


def create_user(name, age):
    user = HelloModel()
    user.name = name
    user.age = age
    user.year = datetime.now().year - int(age) if age else None
    user.background_color = instances.LIGHT_COLOR
    user.text_color = instances.DARK_COLOR
    user.save()
    return


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


def write_user_session(user_sessions, user_id):
    user_data = ju.read_json_file(paths.USER_SESSIONS)
    new_user = instances.NEW_USER.copy()
    new_user.update(user_sessions)

    if new_user[instances.AGE_key]:
        today = datetime.today().year
        age = int(new_user[instances.AGE_key])
        new_user[instances.YEAR_key] = str(today - age)

    user_data[user_id] = {}
    user_data[user_id].update(new_user)
    ju.update_json_file(user_data, paths.USER_SESSIONS)


def parse_received_data(request) -> Dict[str, str]:
    new_data = {}
    for key, value in request.POST.items():
        if value:
            new_data[key] = value
    return new_data
