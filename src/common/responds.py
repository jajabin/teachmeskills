import logging
from typing import Dict

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from src.common import instances


def respond_200(request, msg) -> HttpResponse:
    response = HttpResponse(msg)
    response.status_code = 200
    return response


def respond_404(request) -> HttpResponse:
    msg = "Error 404: File not found"
    response = HttpResponse(msg)
    response.status_code = 404
    return response


def respond_405(request) -> HttpResponse:
    msg = "Error 405: Method not allowed"
    response = HttpResponse(msg)
    response.status_code = 405
    return response


def respond_418(request) -> HttpResponse:
    msg = "Check the entered data"
    response = HttpResponse(msg)
    response.status_code = 418
    return response


def respond_302(request, redirect_to, user_id) -> HttpResponse:
    response = HttpResponseRedirect(redirect_to)
    response.set_cookie(instances.USER_ID, user_id, max_age=None)
    response.status_code = 302
    return response

