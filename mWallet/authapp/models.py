from django.core.validators import MinLengthValidator
from django.db import models

from accounts.models import Person


class Token(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    token = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(20)],
        help_text='Don\'t change token manually. It\'s exist to reset user password'
    )

    def __str__(self):
        return f'Token for {self.person}'
