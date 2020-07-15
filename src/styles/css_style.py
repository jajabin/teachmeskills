import common.paths as paths
import common.responds as responds

from django.http import HttpResponse


def get_cv_style(request) -> HttpResponse:
    return responds.respond_200(request, paths.CV_STYLE, None, 'text/css')
