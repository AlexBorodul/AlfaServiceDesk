from django.db import migrations
from tickets.factories import EmployeeFactory

def create_employee(apps, schema_editor):
    for _ in range(10):
        EmployeeFactory.create()

class Migration(migrations.Migration):
    dependencies = [
           ('tickets', '0002_add_action_type'),
        ]
    operations = [
        migrations.RunPython(create_employee),
    ]