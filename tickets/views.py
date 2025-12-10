from django.shortcuts import render
from django.contrib.auth import authenticate

# Create your views here.

# def auth(request):
#     if request.method == "GET":
#         user = authenticate(username = request.data['login'], password = request.data['password'])
#         if user:
#             return render(request)
#         raise ValueError
#     else:
#         form = 