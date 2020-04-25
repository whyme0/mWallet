from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm,
    UserCreationForm, SetPasswordForm)

from accounts.models import Person
from base import validators


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = 'Email'


class PasswordChange(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChange, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['class'] = 'old_password'
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].label = 'Confirm new password'


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['password1'].help_text = None

    class Meta:
        model = Person
        fields = [
            'first_name', 'middle_name',
            'last_name', 'email', 'phone_number',
            'living_place', 'birth_date',
            'password1', 'password2',
        ]


class AskEmailForm(forms.Form):
    email = forms.EmailField(
        validators=[
            validators.only_email_exist,
            validators.ban_existing_email,
        ],
        help_text='This email must be already registred.',
    )


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

        self.fields['new_password1'].help_text = ''
