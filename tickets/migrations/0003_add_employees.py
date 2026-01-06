from django.db import migrations
from tickets.models import Office
from tickets.factories import UserFactory, EmployeeFactory
from django.contrib.auth.models import Group
from tickets.groups import create_group


def create_employees(apps, schema_editor):
    author_group = Group.objects.get(name='Author')
    worker_group = Group.objects.get(name='Worker')
    offices = Office.objects.all()
    for office in offices:
        main_worker = EmployeeFactory.create(office = office)
        office.main_worker = main_worker
        main_worker_user = UserFactory.create(employee=main_worker)
        main_worker_user.groups.add(author_group, worker_group)
        for _ in range(3):
            worker = EmployeeFactory.create(office=office, parent = main_worker)
            worker_user = UserFactory.create(employee=worker)
            worker_user.groups.add(author_group, worker_group)
        for _ in range(10):
            employee = EmployeeFactory.create(office=office)
            user = UserFactory.create(employee=employee)
            user.groups.add(author_group)
        

class Migration(migrations.Migration):
    dependencies = [
        ('tickets', '0002_add_office'),
    ]
    operations = [
        migrations.RunPython(create_group),
        migrations.RunPython(create_employees),
    ]
