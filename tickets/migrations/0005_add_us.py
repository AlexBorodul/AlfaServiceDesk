from django.db import migrations
from tickets.models import Employee, User, CategoryType, Office
from django.contrib.auth.models import Group
import yaml

def create_employees_from_yaml(apps, schema_editor, file_path='employees.yaml'):
    author_group = Group.objects.get(name='Author')
    worker_group = Group.objects.get(name='Worker')
    category_types = CategoryType.objects.all()
    with open(file_path, 'r') as file:
        employees_data = yaml.safe_load(file)
        for employee_data in employees_data:
            employee = Employee(
                first_name=employee_data['first_name'],
                second_name=employee_data['second_name'],
                surname=employee_data['surname'],
                email=employee_data['email'],
                office=Office.objects.get(id = employee_data['office']),
                status=employee_data['status']
            )
            employee.save()
            employee.specialization.set(category_types)
            user_employee = User(
                username = employee_data['username'],
                email = employee_data['email'],
                employee = employee,
                )
            user_employee.set_password(employee_data['password'])
            user_employee.groups.add(author_group, worker_group)


class Migration(migrations.Migration):
    dependencies = [
        ('tickets', '0004_add_employees'),
    ]
    operations = [
        migrations.RunPython(create_employees_from_yaml),
    ]