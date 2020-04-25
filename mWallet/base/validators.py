from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from accounts.models import Person
from authapp.models import Token
from base import tools


def only_email_exist(value):
    '''
    Validator allows you to submit the
    form only if the entered email exists
    '''
    try:
        # check if email exist
        Person.objects.get(email=value)
    except Person.DoesNotExist:
        raise ValidationError(
            _('User with this email doesn\'t exist.'),
            params={'value': value},
        )


def check_message(value):
    if len(value.strip()) < 20:
        raise ValidationError(
            _('Your message seems really small, '
              'try to describe problem with more details')
        )


def ban_existing_email(value):
    '''
    Forbid ask again password reset link, while token
    for this email exist.
    '''
    if tools.is_email_exist(value):
        person = Person.objects.get(email=value)
        try:
            Token.objects.get(person=person)
            raise ValidationError(
                _('Password reset link for your account was already sent. Try again later.'),
                params={'value': value},
            )
        except Token.DoesNotExist:
            pass
