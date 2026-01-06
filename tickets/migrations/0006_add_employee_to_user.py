from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('tickets', '0005_employee_role_alter_categorytype_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='employee',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets.employee'),
        ),
    ]