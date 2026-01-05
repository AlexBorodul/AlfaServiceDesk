from django.db import migrations
from django.contrib.auth.models import Group
from tickets.factories import EmployeeFactory, OfficeFactory, CategoryTypeFactory, TaskFactory, UserFactory
from tickets.groups import create_group

def fill_data(apps, schema_editor):
    author_group = Group.objects.get(name='Author')
    worker_group = Group.objects.get(name='Worker')

    # Создание офисов
    offices = [OfficeFactory.create() for _ in range(5)]

    # Создание пользователей
    for i in range(50):
        if i < 39:
            user = UserFactory.create()
            user.groups.add(author_group)
            employee = EmployeeFactory.create(office=offices[i % len(offices)])
        elif i < 49:
            user = UserFactory.create()
            user.groups.add(worker_group, author_group)
            worker = EmployeeFactory.create(office=offices[i % len(offices)])
            worker.specialization.set([CategoryTypeFactory()])
        else: 
            user = UserFactory.create(is_staff=True, is_superuser=True)
            employee = EmployeeFactory.create(office=offices[i % len(offices)])

        if i >= 39:
            for _ in range(2):
                task = TaskFactory.create(author=employee, worker=worker, office=offices[i % len(offices)])

class Migration(migrations.Migration):
    dependencies = [
        ('tickets', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_group),
        migrations.RunPython(fill_data),
    ]
