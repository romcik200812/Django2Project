from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Регистрация и вход (для гостя)
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Личный кабинет (заглушка до ПР 2.2)
    path('cabinet/', views.cabinet, name='cabinet'),
    path('cabinet/create/', views.create_request, name='create_request'),
    path('cabinet/delete/<int:pk>/', views.delete_request, name='delete_request'),

    path('superadmin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('superadmin/requests/<int:pk>/status/', views.change_status, name='change_status'),
    path('superadmin/categories/', views.admin_categories, name='admin_categories'),
    path('superadmin/categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
]