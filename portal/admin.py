from django.contrib import admin
from .models import User, Category, Request

# Регистрируем наши модели в админке
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Request)