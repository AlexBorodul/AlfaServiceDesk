from django.db import migrations
from tickets.models import CategoryType

def create_category_types(apps, schema_editor):
    categories = CategoryType.CATEGORY_CHOICES  
    for category in categories:
        CategoryType.objects.create(name=category[1], description=category[0])

class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_add_office'),
    ]

    operations = [
        migrations.RunPython(create_category_types),
    ]