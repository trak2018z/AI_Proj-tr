from django import forms
from .models import models, Profil
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    location = forms.CharField(required=False, label="Miejsce zamieszkania")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


