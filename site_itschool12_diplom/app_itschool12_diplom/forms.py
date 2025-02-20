from django import forms
from django_registration.forms import RegistrationForm
from .models import Profile

class CustomRegistrationForm(RegistrationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        profile = Profile.objects.create(user=user)
        return user