"""
URL configuration for service_desk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tickets import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("/api/tasks/", views.get_tasks),
    path("/api/tasks/<int:task_id>/", views.get_task),
    path("/api/tasks/<int:task_id>/status", views.get_task),
    path("/api/tasks/<int:task_id>/comment", views.todo),
    path("/api/tasks/<int:task_id>/transfer", views.todo),
    path("/api/tasks/<int:task_id>/attachment", views.todo),
    path("/api/tasks/<int:task_id>/feedback", views.todo),
    path("/api/reports/summary/", views.todo),
    path("/api/categories", views.todo),
    path("/api/offices", views.todo),
    path("/api/employees", views.todo)
]
