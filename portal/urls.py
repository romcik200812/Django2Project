from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Личный кабинет пользователя
    path('cabinet/', views.cabinet, name='cabinet'),
    path('cabinet/create/', views.create_request, name='create_request'),
    path('cabinet/delete/<int:pk>/', views.delete_request, name='delete_request'),

    # ПР 2.3: Панель администратора (изменили префикс!)
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/requests/<int:pk>/status/', views.change_status, name='change_status'),
    path('admin-panel/categories/', views.admin_categories, name='admin_categories'),
    path('admin-panel/categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
]