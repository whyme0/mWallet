from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from accounts.models import Person
from django.db.models import Q


class PhoneOrEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            person = get_user_model().objects.get(email=email)
            if person.check_password(password):
                return person
        except Person.DoesNotExist:
            return None

    def get_user(self, person_pk):
        try:
            return get_user_model().objects.get(pk=person_pk)
        except get_user_model().DoesNotExist:
            return None
