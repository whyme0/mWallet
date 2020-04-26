# https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.db import models


class PersonMixin(models.Model):
    middle_name = models.CharField(
        _('Middle name'),
        max_length=70,
        blank=True,
        validators=[MinLengthValidator(2)]
    )
    birth_date = models.DateField(
        _('Your birth date'),
        blank=True,
        null=True,
    )
    phone_number = PhoneNumberField(
        _('Your phone number'),
        unique=True,
        blank=True,
        error_messages={
            'unique': 'This phone number already exists.',
        },
    )
    living_place = models.CharField(
        _('Your living place'),
        max_length=70,
        blank=True,
    )

    class Meta:
        abstract = True
