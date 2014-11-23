import json
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.template.loader import render_to_string
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.csrf import csrf_exempt


class UserRegistration(View):
    template_name = 'registration/login.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UserRegistration, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password1'])
            auth.login(request, user)
            msg = json.dumps({'status': 'ok'})
            return HttpResponse(msg)
        else:
            html = render_to_string('registration/registration.html',
                                    {'signup_form': form})
            return HttpResponse(html, status=400)


class UserLoginView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UserLoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm()
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            msg = json.dumps({'status': 'ok'})
            return HttpResponse(msg)
        else:
            html = render_to_string('registration/login.html',
                                    {'login_form': form})

            return HttpResponse(html, status=400)


class UserLogoutView(View):

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect('/')


signup = UserRegistration.as_view()
login = UserLoginView.as_view()
logout = UserLogoutView.as_view()
