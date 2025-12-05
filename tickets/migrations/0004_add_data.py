from django.db import migrations
from tickets.factories import EmployeeFactory, OfficeFactory, CategoryTypeFactory, TaskFactory

def fill_data(apps, schema_editor):
    for _ in range(5):
        office = OfficeFactory.create()
        for _ in range(10):
            employee = EmployeeFactory.create(office = office)
            worker = EmployeeFactory.create(office = office)
            worker.specialization.set([CategoryTypeFactory()])
            for _ in range(2):
                task = TaskFactory.create(author = employee, worker = worker, office = office)
class Migration(migrations.Migration):
    dependencies = [
           ('tickets', '0003_alter_office_main_worker_alter_task_status'),
        ]
    operations = [
        migrations.RunPython(fill_data),
    ]