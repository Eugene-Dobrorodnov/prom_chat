from __future__ import unicode_literals
from functools import wraps

from django.http import HttpResponseBadRequest, HttpResponseRedirect


def ajax_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.is_ajax():
            return func(request, *args, **kwargs)
        return HttpResponseBadRequest()
    return wrapper


def login_redirect(function=None, redirect_field_name=None):
    """
    Just make sure the user is authenticated to access a certain ajax view

    Otherwise return a HttpResponse 401 - authentication required
    instead of the 302 redirect of the original Django decorator
    """
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/')
        return _wrapped_view

    if function is None:
        return _decorator
    else:
        return _decorator(function)
