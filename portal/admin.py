from django.contrib import admin
from .models import User, Category, Request

# Регистрируем нашу кастомную модель пользователя
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'is_staff')
    search_fields = ('username', 'full_name')


# Регистрируем категории
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


# Регистрируем заявки
@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description')