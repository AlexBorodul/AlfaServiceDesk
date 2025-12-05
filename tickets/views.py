from django.shortcuts import render
from django.http import HttpResponse
from tickets.models import Employee

# Create your views here.


def get_all_workers(request):
    all_worker = Employee.objects.all()
    return render(request, 'tickets/employee.html', {'all_worker': all_worker}) 
    
