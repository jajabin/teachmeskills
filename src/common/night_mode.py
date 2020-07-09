from typing import Dict

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import src.common.instances as instances
import src.common.paths as paths
import src.utils.json_utils as ju
import src.utils.user_utils as uu
from src.common import responds


@csrf_exempt
def set_night_mode(request, redirect_to: str, _file_content: str = None) -> HttpResponse:
    user_id = uu.get_user_id(request)
    user_session = uu.read_user_session(user_id)
    new_colors = get_colors(user_session[user_id])
    user_session[user_id].update(new_colors)
    ju.update_json_file(user_session, paths.USER_SESSIONS)
    return responds.respond_302(redirect_to, user_id)


def get_colors(user_context: Dict) -> Dict[str, str]:
    user_context[instances.BCKG_COLOR], user_context[instances.TXT_COLOR] = \
        user_context[instances.TXT_COLOR], user_context[instances.BCKG_COLOR]
    return user_context
