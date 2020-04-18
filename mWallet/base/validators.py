from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from accounts.models import Person


def email_exist(value):
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
