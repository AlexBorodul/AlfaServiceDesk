from django.db import migrations
from tickets.models import Office

offices = {
    "8 Марта 10": {
        "name": "Альфа Банк, ул. 8 Марта, 10",
        "parent": None,
        "address": "ул. 8 Марта, 10",
        "type": "Банк",
        "work_time": "10:00 - 20:00",
        "main_worker": None
    },
    "Горького 7": {
        "name": "Альфа Банк, ул. Горького, 7а",
        "parent": None,
        "address": "ул. Горького, 7а",
        "type": "Банк",
        "work_time": "10:00 - 19:00",
        "main_worker": None
    },
    "Ленина 60": {
        "name": "Альфа Банк, Проспект Ленина, 60",
        "parent": None,
        "address": "Проспект Ленина, 60",
        "type": "Банк",
        "work_time": "10:00 - 19:00",
        "main_worker": None
    },
    "Сони Морозовой 190": {
        "name": "Альфа Банк, ул. Сони Морозовой, 190",
        "parent": None,
        "address": "улица Сони Морозовой, 190",
        "type": "Банк",
        "work_time": "9:00 - 20:00",
        "main_worker": None
    },
    "8 Марта 194": {
        "name": "Альфа Банк, ул. 8 Марта, 194",
        "parent": None,
        "address": "ул. 8 Марта, 194",
        "type": "Банк",
        "work_time": "10:00 - 19:00",
        "main_worker": None
    },
    "Уральская 75": {
        "name": "Альфа Банк, ул. Уральская, 75",
        "parent": None,
        "address": "ул. Уральская, 75",
        "type": "Банк",
        "work_time": "09:00 - 19:00",
        "main_worker": None
    },
    "Белореченская 12": {
        "name": "Альфа Банк, ул. Уральская, 75",
        "parent": None,
        "address": "ул. Уральская, 75",
        "type": "Банк",
        "work_time": "09:00 - 19:00",
        "main_worker": None
    },
    "Крауля 44": {
        "name": "Альфа Банк, ул. Крауля, 44",
        "parent": None,
        "address": "ул. Крауля, 44",
        "type": "Банк",
        "work_time": "09:00 - 19:00",
        "main_worker": None
    },
    "Родонитовая 4": {
        "name": "Альфа Банк, ул. Родонитовая, 4",
        "parent": None,
        "address": "ул. Родонитовая, 4",
        "type": "Банк",
        "work_time": "10:00 - 20:00",
        "main_worker": None
    },
    "Кузнецова 2": {
        "name": "Альфа Банк, ул. Кузнецова, 2",
        "parent": None,
        "address": "ул. Кузнецова, 2",
        "type": "Банк",
        "work_time": "09:00 - 19:00",
        "main_worker": None
    },
    "Химиков 3": {
        "name": "Альфа Банк, ул. Химиков, 3",
        "parent": None,
        "address": "ул. Химиков, 3",
        "type": "Банк",
        "work_time": "09:00 - 19:00",
        "main_worker": None
    },
    "Вильгельма де Геннина 31": {
        "name": "Альфа Банк, ул. Вильгельма де Геннина, 31",
        "parent": None,
        "address": "ул. Вильгельма де Геннина, 31",
        "type": "Банк",
        "work_time": "10:00 - 20:00",
        "main_worker": None
    },
    "Машиностроителей 19": {
        "name": "Альфа Банк, ул. Машиностроителей, 19",
        "parent": None,
        "address": "ул. Машиностроителей, 19",
        "type": "Банк",
        "work_time": "09:00 - 19:00",
        "main_worker": None
    },
    "Восточная 11, Берёзовский": {
        "name": "Альфа Банк, Восточная 11, Берёзовский",
        "parent": None,
        "address": "ул. Восточная, 11, Берёзовский",
        "type": "Банк",
        "work_time": "10:00 - 20:00",
        "main_worker": None
    },
    "Успенский проспект 20, Верхняя Пышма": {
        "name": "Альфа Банк, пр. Успенский, 20, Верхняя Пышма",
        "parent": None,
        "address": "пр. Успенский, 20, Верхняя Пышма",
        "type": "Банк",
        "work_time": "09:00 - 19:00",
        "main_worker": None
    }
}

def create_offices(apps, schema_editor):
    main_office = Office.objects.create(**offices.pop("8 Марта 10"))
    for office in offices.values():
        office = Office.objects.create(**office)
        office.parent = main_office
        office.save()

class Migration(migrations.Migration):
    dependencies = [
        ('tickets', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_offices),
    ]
