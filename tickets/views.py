from django.shortcuts import render
from django.http import HttpResponse
from tickets.models import Employee

# Create your views here.


def get_all_employees(request):
    employees = Employee.objects.all()
    print(employees)
    return render(request, 'tickets/employees.html', {'employees': employees}) 
    
def get_employee_by_id(request, employee_id):
    employee = Employee.objects.filter(id = employee_id).first()
    print(employee)
    return render(request, 'tickets/employee.html', {"employee": employee})