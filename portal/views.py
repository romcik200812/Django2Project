from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, RequestForm
from .models import Request


# ... (функции home, register, user_login, user_logout оставляем как были) ...

def home(request):
    done_requests = Request.objects.filter(status='done').order_by('-created_at')[:4]
    in_progress_count = Request.objects.filter(status='in_progress').count()
    context = {'done_requests': done_requests, 'in_progress_count': in_progress_count}
    return render(request, 'portal/home.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('cabinet')
    else:
        form = RegisterForm()
    return render(request, 'portal/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('cabinet')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'portal/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


# ============ НОВЫЙ ФУНКЦИОНАЛ ПР 2.2 ============

@login_required
def cabinet(request):
    """Просмотр своих заявок с фильтрацией"""
    # Получаем только заявки текущего пользователя, сортируем по дате (новые сверху)
    user_requests = Request.objects.filter(user=request.user).order_by('-created_at')

    # Фильтрация по статусу (если передан параметр ?status=...)
    status_filter = request.GET.get('status')
    if status_filter:
        user_requests = user_requests.filter(status=status_filter)

    context = {
        'requests': user_requests,
        'status_filter': status_filter,
    }
    return render(request, 'portal/cabinet.html', context)


@login_required
def create_request(request):
    """Создание заявки"""
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)  # request.FILES нужен для фото
        if form.is_valid():
            req = form.save(commit=False)  # Не сохраняем сразу в БД
            req.user = request.user  # Привязываем заявку к пользователю
            req.status = 'new'  # Статус по ТЗ
            req.save()  # Теперь сохраняем
            messages.success(request, 'Заявка успешно создана!')
            return redirect('cabinet')
    else:
        form = RequestForm()
    return render(request, 'portal/create_request.html', {'form': form})


@login_required
def delete_request(request, pk):
    """Удаление заявки"""
    # Получаем заявку, проверяем, что она принадлежит пользователю
    req = get_object_or_404(Request, pk=pk, user=request.user)

    # По ТЗ: удалить можно только если статус "Новая"
    if req.status != 'new':
        messages.error(request, 'Нельзя удалить заявку, которая уже в работе или выполнена.')
        return redirect('cabinet')

    if request.method == 'POST':
        req.delete()
        messages.success(request, 'Заявка удалена.')
        return redirect('cabinet')

    return render(request, 'portal/confirm_delete.html', {'req': req})