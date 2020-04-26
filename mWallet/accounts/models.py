from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils import timezone
from django.db import models

from .managers import PersonManager
from .mixins import PersonMixin


class Person(AbstractBaseUser, PermissionsMixin, PersonMixin):
    first_name = models.CharField(
        _('Your name'),
        max_length=30,
        blank=True,
        validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        _('Your surname'),
        max_length=40,
        blank=True,
        validators=[MinLengthValidator(2)]
    )
    email = models.EmailField(
        _('Your email'),
        unique=True,
        error_messages={
            'unique': 'This email already exists.'
        },
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether person can log into the admin site'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this person should be treated as active.'
            ' Unselect this instead of deleting accounts.'
        ),
    )
    created_date = models.DateTimeField(default=timezone.now)

    objects = PersonManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = '%s %s %s' % (
            self.first_name,
            self.middle_name,
            self.last_name
        )
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Wallet(models.Model):
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(_('Name of your wallet'), max_length=40)
    description = models.TextField(
        _('Description for current wallet'),
        help_text='Maximum 300 letters available',
        max_length=300,
    )
    balance = models.DecimalField(
        _('Your current balance'),
        decimal_places=2,
        max_digits=11,
        default=0.00,
    )
    currency = models.CharField(
        _('Wallet currency'),
        max_length=8,
        choices=[
            ('₽', 'RUB'),
            ('₴', 'UAH'),
            ('$', 'USD'),
            ('€', 'EUR'),
            ('£', 'GBP'),
        ],
        default=None,
    )

    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Wallet: %s' % self.name

    def get_balance(self):
        return '%s%s' % (self.currency, self.balance)


class Operation(models.Model):
    '''
    Operation class stand for determine payment and repayment
    '''
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(
        _('Money payment/repayment amount'),
        decimal_places=2,
        max_digits=11,
        default=0.00,
    )

    description = models.TextField(
        _('Description for your payment/repayment'),
        max_length=100,
        help_text=('100 letters max length.'),
    )

    # decide will it be payment or repayment
    option = models.CharField(
        _('Operation type'),
        max_length=13,
        choices=[('PAYMENT', 'Payment'), ('REPLINISHMENT', 'Replinishment')],
    )

    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.option}: {self.pk}'

    def get_amount(self):
        return '{}{}'.format(self.wallet.currency, self.amount)

    def clean(self):
        """
        Validate option field
        """
        if self.option == 'REPLINISHMENT':
            # check, if the payment amount + wallet balance will be
            # more than wallet can accommodate
            if len(str(self.amount + self.wallet.balance)) > 12:
                raise ValidationError(
                    {'amount': 'There is no more space in the wallet.'}
                )
        elif self.option == 'PAYMENT':
            if self.amount > self.wallet.balance:
                raise ValidationError(
                    {'amount': 'The amount of payment is more than you have on your wallet.'}
                )

    def save(self, *args, **kwargs):
        if self.option == 'PAYMENT':
            self.wallet.balance = self.wallet.balance - self.amount
        elif self.option == 'REPLINISHMENT':
            self.wallet.balance = self.wallet.balance + self.amount

        self.wallet.save()
        return super().save(*args, **kwargs)
