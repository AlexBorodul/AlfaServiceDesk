from django.db import migrations
from tickets.factories import ActionTypeFactory

def create_action_type(apps, schema_editor):
    for _ in range(10):
        ActionTypeFactory.create()

class Migration(migrations.Migration):
    dependencies = [
           ('tickets', '0001_initial'),
        ]
    operations = [
        migrations.RunPython(create_action_type),
    ]