from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import Request


# ============ ГЛАВНАЯ СТРАНИЦА (доступна гостю) ============
def home(request):
    """
    Главная страница.
    Показывает 4 последние выполненные заявки и счётчик заявок в работе.
    """
    done_requests = Request.objects.filter(status='done').order_by('-created_at')[:4]
    in_progress_count = Request.objects.filter(status='in_progress').count()

    context = {
        'done_requests': done_requests,
        'in_progress_count': in_progress_count,
    }
    return render(request, 'portal/home.html', context)


# ============ РЕГИСТРАЦИЯ (доступна гостю) ============
def register(request):
    """
    Регистрация нового пользователя.
    Вся валидация на стороне сервера (в RegisterForm).
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # сохраняем пользователя
            login(request, user)  # автоматически входим
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('cabinet')  # перенаправляем в личный кабинет
    else:
        form = RegisterForm()

    return render(request, 'portal/register.html', {'form': form})


# ============ ВХОД (доступен гостю) ============
def user_login(request):
    """
    Вход в личный кабинет по логину и паролю.
    При неверных данных — сообщение об ошибке.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cabinet')  # успешный вход -> личный кабинет
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()

    return render(request, 'portal/login.html', {'form': form})


# ============ ВЫХОД (доступен авторизованному) ============
def user_logout(request):
    """Выход из профиля"""
    logout(request)
    return redirect('home')


# ============ ЛИЧНЫЙ КАБИНЕТ (заглушка до ПР 2.2) ============
@login_required  # декоратор: доступ только авторизованным
def cabinet(request):
    """
    Личный кабинет пользователя.
    Пока заглушка — полноценный функционал будет в ПР 2.2.
    """
    return render(request, 'portal/cabinet.html', {})