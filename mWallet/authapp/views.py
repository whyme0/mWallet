from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.views.decorators.cache import never_cache
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

from settings import settings
from . import forms


def log_out(request):
    logout(request)

    messages.success(request, 'You\'re successfully loged out.')
    return redirect('home')


class RegistrationView(FormView):
    form_class = forms.RegistrationForm
    template_name = 'authapp/registration.html'

    def form_valid(self, form):
        # after succefull registration person
        # sign in system and redirect to
        # profile page
        return None


class LoginView(FormView):
    template_name = 'authapp/login.html'
    form_class = forms.LoginForm
    extra_context = {'title': 'Login'}

    def form_valid(self, form):
        person = authenticate(
            self.request,
            email=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        login(
            self.request,
            person,
            backend='authapp.authentication.PhoneOrEmailBackend'
        )

        if form.cleaned_data['remember_me'] is True:
            self.request.session.set_expiry(60 * 60 * 24 * 365)

        messages.success(self.request, 'You successfully logged in.')
        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse_lazy('profiles:current_profile')

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('next'):
            message = 'You must sign in before see this page'
            self.extra_context['error_message'] = message
        else:
            self.extra_context['error_message'] = ''
        return super().get(request, *args, **kwargs)


class PasswordChangeView(PasswordChangeView):
    template_name = 'authapp/password-change.html'
    extra_context = {'title': 'Password change'}
    form_class = forms.PasswordChange

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse_lazy('home')
