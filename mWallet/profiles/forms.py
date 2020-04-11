from django import forms
from accounts.models import Person, Wallet, Operation


class PersonEditForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'middle_name',
            'last_name', 'email', 'phone_number',
            'living_place', 'birth_date',
        ]


class WalletCreationForm(forms.ModelForm):
    class Meta:
        model = Wallet
        exclude = ['owner', 'created_date']


class WalletEditForm(forms.ModelForm):
    class Meta:
        model = Wallet
        exclude = ['owner', 'created_date']


class OperationCreateForm(forms.ModelForm):
    class Meta:
        model = Operation
        exclude = ['date']
