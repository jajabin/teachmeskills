import src.common.paths as paths
import src.common.responds as responds
import src.utils.file_utils as fu

from django.http import HttpResponse


def get_cv_style(request) -> HttpResponse:
    return responds.respond_200(request, paths.CV_STYLE, None, 'text/css')
