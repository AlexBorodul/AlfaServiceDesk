# tickets/migrations/0004_add_employees.py (исправленная версия)

from django.db import migrations
from tickets.factories import UserFactory, EmployeeFactory
from django.contrib.auth.models import Group


def create_employees(apps, schema_editor):
    # Используем apps.get_model для безопасного получения моделей
    Group = apps.get_model('auth', 'Group')
    Office = apps.get_model('tickets', 'Office')
    CategoryType = apps.get_model('tickets', 'CategoryType')
    Employee = apps.get_model('tickets', 'Employee')
    User = apps.get_model('tickets', 'User')

    try:
        author_group = Group.objects.get(name='Author')
        worker_group = Group.objects.get(name='Worker')
    except Group.DoesNotExist:
        print("Группы еще не созданы. Пропускаем создание сотрудников.")
        return

    offices = Office.objects.all()
    category_types = CategoryType.objects.all()

    for office in offices:
        # Создаем главного исполнителя
        main_worker = Employee.objects.create(
            first_name="Главный",
            second_name="Исполнитель",
            surname="Офиса",
            email=f"main_worker_{office.id}@example.com",
            office=office,
            status="FREE",
            role="worker"
        )
        main_worker.specialization.set(category_types)
        office.main_worker = main_worker
        office.save()

        # Создаем пользователя для главного исполнителя
        main_worker_user = User.objects.create_user(
            username=f"main_worker_{office.id}",
            email=f"main_worker_{office.id}@example.com",
            password="123",
            employee=main_worker
        )
        main_worker_user.groups.add(author_group, worker_group)

        # Создаем обычных исполнителей
        for i in range(3):
            worker = Employee.objects.create(
                first_name=f"Исполнитель_{i + 1}",
                second_name="Офиса",
                surname=f"{office.id}",
                email=f"worker_{office.id}_{i}@example.com",
                office=office,
                parent=main_worker,
                status="FREE",
                role="worker"
            )
            # Добавляем специализации (случайные 2 категории)
            worker.specialization.set(category_types.order_by('?')[:2])

            worker_user = User.objects.create_user(
                username=f"worker_{office.id}_{i}",
                email=f"worker_{office.id}_{i}@example.com",
                password="123",
                employee=worker
            )
            worker_user.groups.add(author_group, worker_group)

        # Создаем обычных сотрудников
        for i in range(10):
            employee = Employee.objects.create(
                first_name=f"Сотрудник_{i + 1}",
                second_name="Офиса",
                surname=f"{office.id}",
                email=f"employee_{office.id}_{i}@example.com",
                office=office,
                role="employee"
            )

            user = User.objects.create_user(
                username=f"employee_{office.id}_{i}",
                email=f"employee_{office.id}_{i}@example.com",
                password="123",
                employee=employee
            )
            user.groups.add(author_group)


class Migration(migrations.Migration):
    dependencies = [
        ('tickets', '0003_add_category'),
    ]
    operations = [
        migrations.RunPython(create_employees),
    ]