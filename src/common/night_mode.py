from typing import Dict

import src.common.instances as instances
import src.common.paths as paths
import src.common.responds as responds
import src.utils.cookies_utils as cu
import src.utils.json_utils as ju
import src.utils.user_utils as uu


def set_night_mode(server_inst, endpoint: str, _file_content=""):
    user_id = uu.get_user_id(server_inst)
    user_session = uu.read_user_session(user_id)
    new_colors = get_colors(user_session[user_id])
    user_session[user_id].update(new_colors)
    ju.update_json_file(user_session, paths.USER_SESSIONS)
    cookie_master = cu.set_cookies(server_inst, {instances.USER_ID: user_id})
    responds.respond_302(server_inst, endpoint, cookie_master)


def get_colors(user_context: Dict) -> Dict[str, str]:
    user_context[instances.BCKG_COLOR], user_context[instances.TXT_COLOR] = \
        user_context[instances.TXT_COLOR], user_context[instances.BCKG_COLOR]
    return user_context
