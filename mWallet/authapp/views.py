from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
# from django.http import Http404

from authapp.models import Token
from . import forms
from . import tools

from base.tools import send_yandex_email, get_random_key
from accounts.models import Person


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

        # session of user which pushed checkbox
        # button will last for 1 year
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


class AskEmailView(FormView):
    '''
    View with form that ask email from user
    and if this email exist send password
    reset link for this user
    '''
    template_name = 'authapp/ask-email.html'
    form_class = forms.AskEmailForm
    extra_context = {
        'title': 'Ask email'
    }

    def form_valid(self, form):
        token = get_random_key()
        body = f'''\
        Hello, this is your password reset link:
        {self.get_absolute_url() + token}

        If you don't ask for any reset link, just ignore this message.
        '''.strip()

        token_class = Token(
            person=Person.objects.get(email=form.cleaned_data['email']),
            token=token,
        )
        token_class.save()

        tools.start_token_delete(token)
        send_yandex_email(
            'fancydresscostume@yandex.ru',
            'Password reset',
            body,
        )

        messages.success(self.request, 'We sent password reset link to you. Check out your email.')
        return redirect('authapp:ask_email')

    def get_absolute_url(self):
        return 'http://localhost:8000' + str(reverse_lazy('authapp:ask_email'))


class PasswordResetView(TemplateView):
    template_name = 'authapp/password-reset.html'

    def get(self, request, *args, **kwargs):
        try:
            token = self.get_token()
        except Token.DoesNotExist:
            messages.error(
                self.request,
                'Such password reset token doesn\'t exist anymore. Ask for new one.',
                extra_tags='token-404',
            )
            return redirect('authapp:ask_email')

        form = forms.CustomSetPasswordForm(token.person)

        ctx = self.get_context_data(*args, **kwargs)
        ctx['form'] = form
        return render(self.request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        try:
            token = self.get_token()
        except Token.DoesNotExist:
            messages.error(
                self.request,
                'Such password reset token doesn\'t exist anymore. Ask for new one.',
                extra_tags='token-404',
            )
            return redirect('authapp:ask_email')

        form = forms.CustomSetPasswordForm(token.person, self.request.POST)
        if form.is_valid():
            logout(self.request)

            form.save()

            token.delete()
            messages.success(self.request, 'Your passsword was successfully resotred.')
            return redirect('authapp:login')

        ctx = self.get_context_data(*args, **kwargs)
        ctx['form'] = form
        return render(self.request, self.template_name, ctx)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['title'] = 'Password reset'
        return ctx

    def get_token(self):
        return Token.objects.get(token=self.kwargs['token'])
