import project.utils.paths as paths
import project.utils.responds as responds

from django.http import HttpResponse


def get_cv_style(request) -> HttpResponse:
    return responds.respond_200(request, paths.CSS_STYLE, None, 'text/css')
