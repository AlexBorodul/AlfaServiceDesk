from django.db import migrations
from tickets.factories import EmployeeFactory, OfficeFactory, CategoryTypeFactory

def create_employee(apps, schema_editor):
    for _ in range(5):
        office = OfficeFactory.create()
        for _ in range(10):
            employee = EmployeeFactory.create(office = office)
            employee.specialization.set([CategoryTypeFactory()])
class Migration(migrations.Migration):
    dependencies = [
           ('tickets', '0002_add_action_type'),
        ]
    operations = [
        migrations.RunPython(create_employee),
    ]