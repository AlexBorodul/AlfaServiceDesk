from django.shortcuts import render
from django.http import HttpResponse
from tickets.models import Employee

# Create your views here.


def get_all_employees(request):
    employees = Employee.objects.all()
    print(employees)
    return render(request, 'tickets/employee.html', {'employees': employees}) 
    
