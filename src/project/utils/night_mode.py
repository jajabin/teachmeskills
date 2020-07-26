from typing import Dict

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import project.utils.instances as instances


@csrf_exempt
def set_night_mode(request, redirect_to: str) -> HttpResponse:
    switch_colors(request)
    return HttpResponseRedirect(redirect_to)


def switch_colors(request) -> Dict[str, str]:
    current_theme = get_theme(request)
    current_theme[instances.BCKG_COLOR], current_theme[instances.TXT_COLOR] = (
        current_theme[instances.TXT_COLOR],
        current_theme[instances.BCKG_COLOR],
    )
    request.session["theme"] = current_theme


def get_theme(request):
    return request.session.get("theme", instances.DEFAULT_THEMA)
