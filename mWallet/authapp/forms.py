from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm,
    UserCreationForm,)

from accounts.models import Person


class LoginForm(AuthenticationForm):
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
