from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, RequestForm
from .models import Request, Category
from django.contrib.admin.views.decorators import staff_member_required

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


@staff_member_required  # Доступ только для администраторов (is_staff=True)
def admin_dashboard(request):
    """Панель администратора: список всех заявок"""
    all_requests = Request.objects.all().order_by('-created_at')

    # Фильтрация по статусу (опционально)
    status_filter = request.GET.get('status')
    if status_filter:
        all_requests = all_requests.filter(status=status_filter)

    context = {
        'requests': all_requests,
        'status_filter': status_filter,
        'total_count': Request.objects.count(),
        'new_count': Request.objects.filter(status='new').count(),
        'in_progress_count': Request.objects.filter(status='in_progress').count(),
        'done_count': Request.objects.filter(status='done').count(),
    }
    return render(request, 'portal/admin_dashboard.html', context)


@staff_member_required
def change_status(request, pk):
    """Смена статуса заявки администратором"""
    req = get_object_or_404(Request, pk=pk)

    # По ТЗ: менять статус можно только у заявок со статусом "Новая"
    if req.status != 'new':
        messages.error(request, 'Можно менять статус только у заявок со статусом "Новая".')
        return redirect('admin_dashboard')

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status == 'in_progress':
            # Обязательный комментарий
            comment = request.POST.get('comment', '').strip()
            if not comment:
                messages.error(request, 'Для статуса "Принято в работу" необходим комментарий.')
                return render(request, 'portal/change_status.html', {'req': req})
            req.comment = comment
            req.status = 'in_progress'

        elif new_status == 'done':
            # Обязательное изображение дизайна
            design_image = request.FILES.get('design_image')
            if not design_image:
                messages.error(request, 'Для статуса "Выполнено" необходимо прикрепить изображение дизайна.')
                return render(request, 'portal/change_status.html', {'req': req})

            # Проверка формата и размера (как в RequestForm)
            ext = design_image.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'bmp']:
                messages.error(request, 'Допустимые форматы: jpg, jpeg, png, bmp')
                return render(request, 'portal/change_status.html', {'req': req})

            if design_image.size > 2 * 1024 * 1024:
                messages.error(request, 'Размер файла не должен превышать 2 МБ')
                return render(request, 'portal/change_status.html', {'req': req})

            req.design_image = design_image
            req.status = 'done'
        else:
            messages.error(request, 'Недопустимый статус.')
            return redirect('admin_dashboard')

        req.save()
        messages.success(request, f'Статус заявки "{req.title}" изменен на "{req.get_status_display()}".')
        return redirect('admin_dashboard')

    return render(request, 'portal/change_status.html', {'req': req})


@staff_member_required
def admin_categories(request):
    """Управление категориями: список, добавление"""
    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            # Проверка на дубликат
            if Category.objects.filter(name=name).exists():
                messages.error(request, f'Категория "{name}" уже существует.')
            else:
                Category.objects.create(name=name)
                messages.success(request, f'Категория "{name}" добавлена.')
            return redirect('admin_categories')
        else:
            messages.error(request, 'Название категории не может быть пустым.')

    context = {
        'categories': categories,
        'total_categories': categories.count(),
    }
    return render(request, 'portal/admin_categories.html', context)


@staff_member_required
def delete_category(request, pk):
    """Удаление категории и всех её заявок"""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        # По ТЗ: при удалении категории удаляются все заявки этой категории
        requests_count = Request.objects.filter(category=category).count()
        category.delete()  # Cascade удалит все связанные заявки

        messages.success(request, f'Категория удалена. Удалено заявок: {requests_count}.')
        return redirect('admin_categories')

    return render(request, 'portal/confirm_delete_category.html', {'category': category})