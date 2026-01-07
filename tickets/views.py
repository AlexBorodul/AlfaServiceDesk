from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from tickets.models import Task, CategoryType, Employee, User, Commentary, Attachment, Action, Feedback
from tickets.forms import TaskForm, SendEmailForm, FeedbackForm
import json
from datetime import datetime


def get_current_employee(request):
    """Получение текущего сотрудника"""
    if request.user.is_authenticated:
        try:
            return request.user.employee
        except:
            return None
    return None


def login_view(request):
    """Авторизация - исправленная версия"""
    if request.user.is_authenticated:
        return redirect('tickets:tasks')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')

            # Проверяем, есть ли Employee у пользователя
            try:
                employee = user.employee
                if employee:
                    # Сохраняем информацию о сотруднике в сессии
                    request.session['employee_id'] = employee.id
                    request.session['employee_name'] = f"{employee.first_name} {employee.second_name or ''}"
                else:
                    # Если Employee нет, создаем его автоматически
                    employee = Employee.objects.create(
                        first_name=user.first_name or user.username,
                        second_name=user.last_name or "",
                        email=user.email,
                        role='employee'
                    )
                    user.employee = employee
                    user.save()

                    request.session['employee_id'] = employee.id
                    request.session['employee_name'] = f"{employee.first_name} {employee.second_name or ''}"

                    messages.info(request, f'Создан профиль сотрудника для {user.username}')
            except Exception as e:
                messages.warning(request, f'Не удалось создать профиль сотрудника: {str(e)}')

            # Редирект
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('tickets:tasks')
        else:
            messages.error(request, 'Неверные учетные данные')
    else:
        form = AuthenticationForm()

    return render(request, 'tickets/login.html', {"form": form})


def logout_view(request):
    """Выход из системы"""
    auth_logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('tickets:login')


@login_required
def create_task(request):
    """Создание новой заявки - исправленная версия"""
    current_employee = get_current_employee(request)

    if not current_employee:
        if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
            messages.warning(request, "Для создания заявки необходимо привязать аккаунт к сотруднику. Обратитесь к администратору или создайте Employee запись.")
            return redirect('tickets:tasks')
        else:
            messages.error(request, "Ваш аккаунт не привязан к сотруднику.")
            return redirect('tickets:tasks')

    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                task = form.save(commit=False)
                task.author = current_employee

                # Если не выбран офис, берем офис сотрудника
                if not task.office and current_employee.office:
                    task.office = current_employee.office

                # Если не выбран исполнитель, пробуем автоматически назначить
                if not task.worker and task.category:
                    from tickets.workerController import WorkerController
                    task = WorkerController.auto_select_worker(task)

                task.save()

                # Обработка прикрепленного файла (один файл)
                file = request.FILES.get('file')
                if file:
                    Attachment.objects.create(
                        task=task,
                        file=file,
                        uploaded_by=current_employee
                    )

                # Записываем действие в историю
                Action.objects.create(
                    task=task,
                    author=current_employee,
                    description=f"Заявка создана"
                )

                messages.success(request, f'Заявка #{task.id} успешно создана!')
                return redirect("task_detail", task_id=task.id)

            except Exception as e:
                messages.error(request, f'Ошибка при создании заявки: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        # Начальные значения формы
        initial_data = {}
        if current_employee.office:
            initial_data['office'] = current_employee.office

        form = TaskForm(initial=initial_data)

    # Получаем доступные категории
    categories = CategoryType.objects.all()

    return render(request, "tickets/create_task.html", {
        "form": form,
        "categories": categories,
        "current_employee": current_employee,
    })


@login_required
def all_tasks(request):
    """Список всех заявок пользователя"""
    current_employee = get_current_employee(request)

    # Для суперпользователей и админов показываем все заявки, если нет Employee
    if not current_employee:
        if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
            # Админы могут видеть все заявки
            tasks = Task.objects.all().order_by('-created_at')
            messages.info(request, "Вы вошли как администратор. Отображаются все заявки.")
        else:
            messages.error(request, "Ваш аккаунт не привязан к сотруднику. Обратитесь к администратору.")
            return render(request, 'tickets/tasks.html', {'tasks': [], 'current_employee': None})
    else:
        # Получаем заявки пользователя
        tasks = Task.objects.filter(author=current_employee).order_by('-created_at')

    context = {
        'tasks': tasks,
        'current_employee': current_employee,
    }

    return render(request, 'tickets/tasks.html', context)


@login_required
def get_task(request, task_id):
    """Детальная страница заявки"""
    task = get_object_or_404(Task, id=task_id)
    current_employee = get_current_employee(request)

    # Проверка доступа к заявке
    is_admin = request.user.is_superuser or request.user.groups.filter(name='Admin').exists()
    
    # Админы могут видеть все заявки даже без Employee
    if not current_employee:
        if is_admin:
            # Админы могут просматривать любую заявку
            pass
        else:
            messages.error(request, "Ваш аккаунт не привязан к сотруднику.")
            return redirect('tickets:tasks')
    else:
        # Для обычных пользователей проверяем права доступа
        if not (is_admin or
                task.author == current_employee or
                task.worker == current_employee):
            messages.error(request, "У вас нет доступа к этой заявке.")
            return redirect('tickets:tasks')

    # Получаем связанные данные
    comments = Commentary.objects.filter(task=task).order_by('created_at')
    actions = Action.objects.filter(task=task).order_by('-created_at')
    attachments = Attachment.objects.filter(task=task).order_by('-uploaded_at')

    # Обработка добавления комментария
    if request.method == 'POST' and 'add_comment' in request.POST:
        if not current_employee:
            messages.warning(request, "Для добавления комментария необходимо привязать аккаунт к сотруднику.")
        else:
            comment_text = request.POST.get('comment_text', '').strip()
            if comment_text:
                Commentary.objects.create(
                    task=task,
                    author=current_employee,
                    text=comment_text
                )
                messages.success(request, 'Комментарий добавлен')
                return redirect('tickets:task_detail', task_id=task.id)

    # Обработка изменения статуса
    if request.method == 'POST' and 'change_status' in request.POST:
        if request.user.is_superuser or request.user.groups.filter(name__in=['Admin', 'Worker']).exists():
            if not current_employee:
                messages.warning(request, "Для изменения статуса необходимо привязать аккаунт к сотруднику.")
            else:
                new_status = request.POST.get('status')
                if new_status in dict(Task.STATUS_CHOICES):
                    old_status = task.status
                    task.status = new_status
                    task.save()

                    Action.objects.create(
                        task=task,
                        author=current_employee,
                        description=f"Статус изменен: {old_status} → {new_status}"
                    )

                    messages.success(request, f'Статус заявки изменен')
                    return redirect('tickets:task_detail', task_id=task.id)

    context = {
        'task': task,
        'comments': comments,
        'actions': actions,
        'attachments': attachments,
        'current_employee': current_employee,
        'can_edit': request.user.is_superuser or
                    request.user.groups.filter(name='Admin').exists() or
                    task.author == current_employee,
        'can_change_status': request.user.is_superuser or
                             request.user.groups.filter(name__in=['Admin', 'Worker']).exists(),
        'status_choices': Task.STATUS_CHOICES,
    }

    return render(request, 'tickets/task.html', context)


def dashboard(request):
    """Дашборд системы"""
    current_employee = get_current_employee(request)

    if not current_employee:
        messages.error(request, "Ваш аккаунт не привязан к сотруднику.")
        return redirect('tickets:login')

    # Простая версия дашборда - перенаправление на заявки
    return redirect('tickets:tasks')


@login_required
@permission_required('tickets.change_task', raise_exception=True)
def edit_task(request, task_id):
    """Редактирование заявки"""
    task = get_object_or_404(Task, id=task_id)
    current_employee = get_current_employee(request)
    is_admin = request.user.is_superuser or request.user.groups.filter(name='Admin').exists()

    if not current_employee:
        if is_admin:
            messages.warning(request, "Для редактирования заявки необходимо привязать аккаунт к сотруднику.")
            return redirect('tickets:task_detail', task_id=task.id)
        else:
            messages.error(request, "Ваш аккаунт не привязан к сотруднику.")
            return redirect('tickets:tasks')

    # Проверка прав на редактирование
    if not (request.user.is_superuser or
            request.user.groups.filter(name='Admin').exists() or
            task.author == current_employee):
        messages.error(request, "У вас нет прав для редактирования этой заявки.")
        return redirect('tickets:task_detail', task_id=task.id)

    if request.method == "POST":
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()

            # Обработка новых файлов
            files = request.FILES.getlist('files')
            for file in files:
                Attachment.objects.create(
                    task=task,
                    file=file,
                    uploaded_by=current_employee
                )

            # Записываем действие
            Action.objects.create(
                task=task,
                author=current_employee,
                description="Заявка отредактирована"
            )

            messages.success(request, f'Заявка #{task.id} обновлена!')
            return redirect("tickets:task_detail", task_id=task.id)
    else:
        form = TaskForm(instance=task)

    # Получаем текущие прикрепленные файлы
    attachments = Attachment.objects.filter(task=task)

    return render(request, "tickets/edit_task.html", {
        "form": form,
        "task": task,
        "attachments": attachments,
        "current_employee": current_employee,
    })


@login_required
def send_message(request):
    """Отправка email"""
    current_employee = get_current_employee(request)

    if not current_employee:
        return redirect('tickets:tasks')

    if request.method == 'POST':
        form = SendEmailForm(request.POST, request.FILES)
        if form.is_valid():
            # Здесь должна быть логика отправки email
            # Например, через Celery task или SMTP

            messages.success(request, 'Сообщение успешно отправлено!')
            return redirect('tickets:tasks')
    else:
        form = SendEmailForm()

    # Получаем список сотрудников для выбора получателя
    employees = Employee.objects.all()

    return render(request, 'tickets/email_form.html', {
        "form": form,
        "employees": employees,
        "current_employee": current_employee,
    })


@login_required
def feedback(request, task_id):
    """Обратная связь по заявке"""
    task = get_object_or_404(Task, id=task_id)
    current_employee = get_current_employee(request)

    if not current_employee:
        return redirect('tasks')

    # Проверяем, может ли пользователь оставлять фидбек
    if task.author != current_employee and not request.user.is_superuser:
        messages.error(request, "Вы можете оставлять отзыв только по своим заявкам.")
        return redirect('tickets:task_detail', task_id=task.id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            feedback_text = form.cleaned_data['feedback']

            # Создаем или обновляем фидбек
            Feedback.objects.update_or_create(
                task=task,
                defaults={
                    'rating': rating,
                    'comment': feedback_text,
                }
            )

            messages.success(request, 'Спасибо за вашу оценку!')
            return redirect('tickets:task_detail', task_id=task.id)
    else:
        form = FeedbackForm()

    return render(request, 'tickets/feedback.html', {
        "form": form,
        "task": task,
        "current_employee": current_employee,
    })


@login_required
def all_users(request):
    """Список всех сотрудников"""
    if not request.user.is_superuser and not request.user.groups.filter(name='Admin').exists():
        messages.error(request, "У вас нет доступа к этой странице.")
        return redirect('tickets:tasks')

    employees = Employee.objects.all().order_by('first_name', 'second_name')

    return render(request, 'tickets/employees.html', {
        'employees': employees,
        'current_employee': get_current_employee(request),
    })


@login_required
def user_by_id(request, user_id):
    """Карточка сотрудника"""
    if not request.user.is_superuser and not request.user.groups.filter(name='Admin').exists():
        messages.error(request, "У вас нет доступа к этой странице.")
        return redirect('tickets:tasks')

    employee = get_object_or_404(Employee, id=user_id)

    # Получаем статистику по заявкам сотрудника
    created_tasks = Task.objects.filter(author=employee).count()
    assigned_tasks = Task.objects.filter(worker=employee).count()
    completed_tasks = Task.objects.filter(worker=employee, status='done').count()

    return render(request, 'tickets/employee.html', {
        'employee': employee,
        'created_tasks': created_tasks,
        'assigned_tasks': assigned_tasks,
        'completed_tasks': completed_tasks,
        'current_employee': get_current_employee(request),
    })


@login_required
def dashboard(request):
    """Дашборд системы"""
    current_employee = get_current_employee(request)

    if not current_employee:
        messages.error(request, "Ваш аккаунт не привязан к сотруднику.")
        return redirect('tickets:login')

    # Статистика для разных ролей
    if request.user.is_superuser or request.user.groups.filter(name='Admin').exists():
        # Админская статистика
        stats = {
            'total_tasks': Task.objects.count(),
            'open_tasks': Task.objects.exclude(status__in=['done', 'rejected']).count(),
            'in_progress': Task.objects.filter(status='in_progress').count(),
            'today_tasks': Task.objects.filter(created_at__date=datetime.today()).count(),
        }
        recent_tasks = Task.objects.all().order_by('-created_at')[:5]

    elif request.user.groups.filter(name='Worker').exists():
        # Статистика для исполнителя
        stats = {
            'total_tasks': Task.objects.filter(worker=current_employee).count(),
            'open_tasks': Task.objects.filter(worker=current_employee).exclude(status__in=['done', 'rejected']).count(),
            'in_progress': Task.objects.filter(worker=current_employee, status='in_progress').count(),
            'today_tasks': Task.objects.filter(worker=current_employee, created_at__date=datetime.today()).count(),
        }
        recent_tasks = Task.objects.filter(worker=current_employee).order_by('-created_at')[:5]

    else:
        # Статистика для обычного сотрудника
        stats = {
            'total_tasks': Task.objects.filter(author=current_employee).count(),
            'open_tasks': Task.objects.filter(author=current_employee).exclude(status__in=['done', 'rejected']).count(),
            'in_progress': Task.objects.filter(author=current_employee, status='in_progress').count(),
            'today_tasks': Task.objects.filter(author=current_employee, created_at__date=datetime.today()).count(),
        }
        recent_tasks = Task.objects.filter(author=current_employee).order_by('-created_at')[:5]

    context = {
        'stats': stats,
        'recent_tasks': recent_tasks,
        'current_employee': current_employee,
        'is_admin': request.user.is_superuser or request.user.groups.filter(name='Admin').exists(),
        'is_worker': request.user.groups.filter(name='Worker').exists(),
    }

    return render(request, 'tickets/dashboard.html', context)