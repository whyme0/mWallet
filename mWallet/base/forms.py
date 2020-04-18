from django.contrib import forms

from . import validators


class FeedbackForm(forms.Form):
    email = forms.EmailField(
        validators=[validators.email_exist],
        help_text='This email must be already registred.',
    )

    feeback_message = forms.CharField(
        validators=[validators.check_empty],
        widget=forms.Textarea,
        help_text='Leave your feedback in this field',
    )
