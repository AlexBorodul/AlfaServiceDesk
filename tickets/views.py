from django.shortcuts import render
from django.contrib.auth import authenticate
from tickets.forms import TaskForm

# Create your views here.

#TODO, Добавить получение токена при помощи TokenObtainPaiView
# def auth(request):
#     if request.method == "GET":
#         user = authenticate(username = request.data['login'], password = request.data['password'])
#         if user:
#             return render(request)
#         raise ValueError
#     else:
#         form = 

def create_task(request):
    form = TaskForm()
    if request.method == "POST":
        task = TaskForm(request.POST)
        if task.is_valid():
            task.save()
    else: 
        return render(request, 'tickets/task.html', {"form": form})