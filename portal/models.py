from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# 1. Модель Пользователя (расширяем стандартного)
class User(AbstractUser):
    full_name = models.CharField(
        max_length=150,
        verbose_name='ФИО',
        validators=[
            RegexValidator(
                regex=r'^[А-Яа-яЁё\s\-]+$',
                message='ФИО должно содержать только кириллицу, пробелы и дефис'
            )
        ]
    )

    def __str__(self):
        return self.full_name


# 2. Модель Категории
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')

    def __str__(self):
        return self.name


# 3. Модель Заявки
class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('done', 'Выполнено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    photo = models.ImageField(upload_to='photos/', verbose_name='Фото помещения')
    design_image = models.ImageField(
        upload_to='designs/',
        blank=True, null=True,
        verbose_name='Изображение дизайна'
    )
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title