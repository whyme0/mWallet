from captcha.fields import ReCaptchaField
from django import forms

from . import validators


class FeedbackForm(forms.Form):
    feedback_title = forms.CharField(label='Title')

    feedback_message = forms.CharField(
        label='Message',
        validators=[validators.check_message],
        widget=forms.Textarea,
        help_text='Leave your feedback in this field',
    )

    email = forms.EmailField(
        validators=[validators.only_email_exist],
        help_text='This email must be already registred.',
    )

    recaptcha = ReCaptchaField(
        required=True,
        error_messages={'required': 'Required!'},
    )
