from django import forms
from accounts.models import Person


class PersonEditForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'first_name', 'middle_name',
            'last_name', 'email', 'phone_number',
            'living_place', 'birth_date',
        ]
