from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from .models import User


class RegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    full_name = forms.CharField(
        max_length=150,
        label='ФИО',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        required=True
    )

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']

    def clean_full_name(self):
        """Проверка ФИО: только кириллица, пробелы и дефис"""
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[А-Яа-яЁё\s\-]+$', full_name):
            raise ValidationError('ФИО должно содержать только кириллицу, пробелы и дефис')
        return full_name

    def clean_username(self):
        """Проверка логина: только латиница и дефис, уникальный"""
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z\-]+$', username):
            raise ValidationError('Логин должен содержать только латиницу и дефис')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean_consent(self):
        """Проверка согласия на обработку ПД"""
        consent = self.cleaned_data.get('consent')
        if not consent:
            raise ValidationError('Необходимо согласие на обработку персональных данных')
        return consent


class LoginForm(AuthenticationForm):
    """Форма входа в систему"""
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )