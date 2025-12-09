from django.shortcuts import render
from django.http import HttpResponse
from tickets.models import Employee, Task
from tickets.forms import TaskForm, SendEmailForm

def all_tasks(request):
    """При POST запросе создаём заявку, при GET-Запросе получаем её"""
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save() 
    elif request.method == 'GET':
        tasks = Task.objects.all()
        return render(request, 'tickets/tasks.html', {"tasks": tasks, "form": form})

def send_message(request):
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SendEmailForm()
    return render(request, 'tickets/email_form.html', {"form": form})

def get_task(request, task_id):
    task = Task.objects.filter(id = task_id).first()
    return render(request, 'tickets/task.html', {'task': task})
    
