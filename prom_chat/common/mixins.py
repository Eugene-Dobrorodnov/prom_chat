from django.utils.decorators import method_decorator
from common.decorators import login_redirect, ajax_required


class LoginRedirectMixin(object):

    @method_decorator(login_redirect)
    def dispatch(self, *args, **kwargs):
        return super(LoginRedirectMixin, self).dispatch(*args, **kwargs)


class AjaxRequiredMixin(object):

    @method_decorator(ajax_required)
    def dispatch(self, *args, **kwargs):
        return super(AjaxRequiredMixin, self).dispatch(*args, **kwargs)