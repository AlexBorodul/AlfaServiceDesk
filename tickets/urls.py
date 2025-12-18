from django.urls import path
from . import views

urlpatterns = [
    # Главная страница и заявки
    path('', views.all_tasks, name='tasks'),  # главная страница
    path('tasks/', views.all_tasks, name='tasks'),  # дублирующий маршрут для уверенности
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.get_task, name='task_detail'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),

    # Аутентификация
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Email и фидбек
    path('send-email/', views.send_message, name='send_email'),
    path('tasks/<int:task_id>/feedback/', views.feedback, name='feedback'),
    path('employees', views.all_users, name='users')
]

