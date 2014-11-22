from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        context['login_form'] = AuthenticationForm()
        context['signup_form'] = UserCreationForm()
        return context