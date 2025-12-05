from django.shortcuts import render
from django.http import HttpResponse
from tickets.models import Employee

# Create your views here.


async def get_all_workers(request):
    first_worker = await Employee.objects.afirst()
    if first_worker:
        html = '<html lang="en"><body>We got one</body></html'
        return HttpResponse(html)
    html = '<html lang="en"><body>No one</body></html'
    return HttpResponse(html)
    
