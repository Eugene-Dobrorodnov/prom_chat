from django.utils.decorators import method_decorator
from common.decorators import login_required_ajax, ajax_required


class LoginRequiredAjaxMixin(object):

    @method_decorator(login_required_ajax)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredAjaxMixin, self).dispatch(*args, **kwargs)


class AjaxRequiredMixin(object):

    @method_decorator(ajax_required)
    def dispatch(self, *args, **kwargs):
        return super(AjaxRequiredMixin, self).dispatch(*args, **kwargs)