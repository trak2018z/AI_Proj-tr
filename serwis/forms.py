from django import forms
from .models import models, Post, Profil
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    location = forms.CharField(required=False, label="Miejsce zamieszkania")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        labels = {
            'tytul': 'Tytuł',
            'tresc': "Treść"
        }
        fields = ('tytul', 'podsumowanie', 'rodzaj', 'tresc', 'obraz')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profil
        labels = {
            'lokacja': 'Lokacja',
            'plec': 'Płeć',
            'wiek': 'Wiek',
        }
        fields = ('lokacja', 'plec', 'wiek',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )
