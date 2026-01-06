from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Office(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=30, blank=True)
    work_time = models.CharField(max_length=100, blank=True)
    main_worker = models.ForeignKey('Employee', null=True, on_delete=models.SET_NULL, related_name='main_of')

    def __str__(self):
        return self.name

class CategoryType(models.Model):
    CATEGORY_CHOICES = [
        ('access/security','Проблемы с доступом и безопасностью'),
        ('software','Проблемы с программным обеспечением'),
        ('reports, statements, documents','Проблемы с отчётами, выписками, документами'),
        ('hardware', 'Проблемы с оборудованием'),
        ('communications/connection', 'Проблемы с коммуникациями и связью'),
        ('service requests', 'Запросы на предоставление услуг')
    ]
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    ROLE_CHOICES = [
        ('employee','Employee'),
        ('worker','Worker'),
        ('admin','Admin')
    ]
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    office = models.ForeignKey(Office, null=True, blank=True, on_delete=models.SET_NULL)
    specialization = models.ManyToManyField(CategoryType, blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(choices = [("FREE", "free"), ("BUSY", "busy")], null = True, blank = True, max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.surname or ''}"

class Task(models.Model):
    STATUS_CHOICES = [
        ('waiting','Ожидает'),
        ('in_progress','В работе'),
        ('done','Завершена'),
        ('rework','Исправление'),
        ('rejected','Отклонена'),
    ]

    PRIORITY_CHOICES = [
        ("low", "Низкий"),
        ("normal", "Обычный"),
        ("high", "Высокий"),
        ("critical", "Критический")
    ]

    title = models.CharField(max_length=200)
    problem = models.TextField()
    author = models.ForeignKey(Employee, related_name='tasks_created', on_delete=models.CASCADE)
    worker = models.ForeignKey(Employee, null=True, blank=True, related_name='tasks_assigned', on_delete=models.SET_NULL)
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES, default='normal')
    category = models.ForeignKey(CategoryType, null=True, blank=True, on_delete=models.SET_NULL)
    office = models.ForeignKey(Office, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"[{self.pk}] {self.title}"

class ActionType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

class Action(models.Model):
    task = models.ForeignKey(Task, related_name='actions', on_delete=models.CASCADE)
    author = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    action_type = models.ForeignKey(ActionType, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Commentary(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Attachment(models.Model):
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
    uploaded_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    task = models.OneToOneField(Task, related_name='feedback', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)  # 1..5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class TimeLog(models.Model):
    task = models.ForeignKey(Task, related_name='timelogs', on_delete=models.CASCADE)
    worker = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    @property
    def duration(self):
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 3600.0
        return None
class User(AbstractUser):
    employee = models.OneToOneField('Employee', null=True, blank=True, on_delete=models.SET_NULL)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  
        blank=True,
    )