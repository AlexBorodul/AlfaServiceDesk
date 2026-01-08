from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import Http404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from tickets.workerController import WorkerController
from tickets.models import Task, CategoryType, Employee, User
from tickets.forms import TaskForm, SendEmailForm, FeedbackForm


def login_view(request):
    """Авторизация"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            try:
                access_token = AccessToken.for_user(user)
                request.session['access_token'] = user.employee.id
            except TokenError:
                messages.error(request, 'Failed to receive tokens')
            return redirect('tasks')
        else:
            messages.error(request, 'Неверные учетные данные')
    else:
        form = AuthenticationForm()

    return render(request, 'tickets/login.html', {"form": form})


def logout_view(request):
    """Выход из системы"""
    auth_logout(request)
    return redirect('login')

@permission_classes([IsAuthenticated])
@login_required
def all_tasks(request):
    """Список всех заявок пользователя"""
    groups_count = request.user.groups.count()
    tasks = Task.objects.filter(author__id=request.session['access_token']).order_by('-created_at')   
    return render(request, 'tickets/tasks.html', {"tasks": tasks, "groups_count": groups_count})

@permission_classes([IsAuthenticated])
@login_required
def all_tasks_workers(request):
    """Список всех заявок пользователя"""
    tasks = Task.objects.filter(worker__id=request.session['access_token']).order_by('-created_at')   
    return render(request, 'tickets/tasks.html', {"tasks": tasks, "groups_count": 2})

@permission_classes([IsAuthenticated])
@login_required
def create_task(request):
    """Создание новой заявки"""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = Employee.objects.get(pk = request.session['access_token'])
            if not task.office:
                task.office = task.author.office
            if not task.worker:
                WorkerController.auto_select_worker(task)
            task.save() 
            return redirect("task_detail", task_id=task.id)
    else:
        form = TaskForm()

    return render(request, "tickets/create_task.html", {
        "form": form,
    })

@permission_classes([IsAuthenticated])
@login_required
def get_task(request, task_id):
    """Детальная страница заявки"""
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tickets/task.html', {'task': task})

@permission_classes([IsAuthenticated])
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            if not task.office:
                task.office = task.author.office
            if not task.worker:
                WorkerController.auto_select_worker(task)
            form.save()
            return redirect("task_detail", task_id=task.id)
    else:
        form = TaskForm(instance=task)

    return render(request, "tickets/edit_task.html", {
        "form": form,
        "task": task
    })

@permission_classes([IsAuthenticated])
@login_required
def send_message(request):
    """Отправка email"""
    if request.method == 'POST':
        form = SendEmailForm(request.POST, request.FILES)
        if form.is_valid():
            # Здесь будет логика отправки email
            messages.success(request, 'Сообщение успешно отправлено!')
            return redirect('tasks')
    else:
        form = SendEmailForm()

    return render(request, 'tickets/email_form.html', {"form": form})

@permission_classes([IsAuthenticated])
@login_required
def feedback(request, task_id):
    """Обратная связь по заявке"""
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Здесь будет логика сохранения фидбека
            messages.success(request, 'Спасибо за вашу оценку!')
            return redirect('task_detail', task_id=task.id)
    else:
        form = FeedbackForm()

    return render(request, 'tickets/feedback.html', {"form": form, "task": task})

@login_required
def all_users(request):
    users = Employee.objects.all()
    return render(request, 'tickets/employees.html', {'employees': users})


@login_required
def user_by_id(request, user_id):
    users = Employee.objects.get(pk = user_id)
    return render(request, 'tickets/employee.html', {'employee': users})
