from django.shortcuts import render
from django.http import HttpResponse
from tickets.models import Employee, Task
from tickets.forms import TaskForm, SendEmailForm

# Create your views here.


def get_all_employees(request):
    employees = Employee.objects.all()
    return render(request, 'tickets/employees.html', {'employees': employees}) 
    
def get_employee_by_id(request, employee_id):
    employee = Employee.objects.filter(id = employee_id).first()
    return render(request, 'tickets/employee.html', {"employee": employee})

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем задачу в базе данных
    else:
        form = TaskForm()  # Создаем пустую форму

    return render(request, 'tickets/create_task.html', {'form': form})

def send_message(request):
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SendEmailForm()
    return render(request, 'tickets/email_form.html', {"form": form})


def get_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'tickets/tasks.html', {"tasks": tasks})