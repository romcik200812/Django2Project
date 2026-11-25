from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from .models import User
from .models import Request


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


class RequestForm(forms.ModelForm):
    """Форма создания заявки"""

    class Meta:
        model = Request
        fields = ['title', 'description', 'category', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_photo(self):
        """Проверка фото: формат и размер (ТЗ)"""
        photo = self.cleaned_data.get('photo')
        if photo:
            # 1. Проверка формата
            ext = photo.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'bmp']:
                raise ValidationError('Допустимые форматы: jpg, jpeg, png, bmp')

            # 2. Проверка размера (2 МБ = 2 * 1024 * 1024 байт)
            if photo.size > 2 * 1024 * 1024:
                raise ValidationError('Размер файла не должен превышать 2 МБ')
        return photo