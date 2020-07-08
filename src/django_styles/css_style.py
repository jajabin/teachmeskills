import src.django_common.paths as paths
import src.django_common.responds as responds
import src.django_utils.file_utils as fu

from django.http import HttpResponse


def get_cv_style(_request) -> HttpResponse:
    msg = fu.get_file_contents(paths.CV_STYLE)

    response = HttpResponse(msg, content_type='text/css')
    response['Content-Length'] = len(msg)

    return response
