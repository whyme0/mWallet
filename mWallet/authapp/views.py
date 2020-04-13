from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import FormView
from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

from .authentication import PhoneOrEmailBackend
from .forms import LoginForm, PasswordChange


def log_out(request):
    logout(request)

    messages.success(request, 'You\'re successfully loged out.')
    return redirect('home')


class LoginView(FormView):
    template_name = 'authapp/login.html'
    form_class = LoginForm
    extra_context = {'title': 'Login'}

    def form_valid(self, form):
        person = PhoneOrEmailBackend().authenticate(
            self.request,
            email=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        login(self.request, person, backend='authapp.authentication.PhoneOrEmailBackend')
        messages.success(self.request, 'You successfully logged in.')

        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse_lazy('profiles:current_profile')


class PasswordChangeView(PasswordChangeView):
    template_name = 'authapp/password-change.html'
    extra_context = {'title': 'Password change'}
    form_class = PasswordChange

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return reverse_lazy('home')
