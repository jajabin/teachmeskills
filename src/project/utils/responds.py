from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from project.utils import instances


def respond_200(request, file, context, content_type="text/html") -> HttpResponse:
    return render(request, file, context, content_type)


def respond_404() -> HttpResponse:
    msg = "Error 404: File not found"
    response = HttpResponse(msg)
    response.status_code = 404
    return response


def respond_405() -> HttpResponse:
    msg = "Error 405: Method not allowed"
    response = HttpResponse(msg)
    response.status_code = 405
    return response


def respond_418() -> HttpResponse:
    msg = "Check the entered data"
    response = HttpResponse(msg)
    response.status_code = 418
    return response


def respond_302(redirect_to, user_id) -> HttpResponse:
    response = HttpResponseRedirect(redirect_to)
    response.set_cookie(instances.USER_ID, user_id, max_age=None)
    response.status_code = 302
    return response
