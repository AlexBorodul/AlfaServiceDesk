from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from tickets.models import Task


def create_group(apps, schema_editor):
    # Используем apps.get_model для получения моделей во время миграции
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth', 'Permission')
    Group = apps.get_model('auth', 'Group')

    # Получаем ContentType для модели Task
    try:
        content_type = ContentType.objects.get_for_model(Task)
    except:
        # Если ContentType еще не создан, используем альтернативный подход
        content_type = ContentType.objects.filter(app_label='tickets', model='task').first()
        if not content_type:
            # Создаем ContentType если его нет
            content_type = ContentType.objects.create(
                app_label='tickets',
                model='task',
                name='Task'
            )

    # Создаем группы только если они не существуют
    author_group, created = Group.objects.get_or_create(name="Author")
    worker_group, created = Group.objects.get_or_create(name="Worker")
    admin_group, created = Group.objects.get_or_create(name="Admin")

    # Создаем разрешения только если они не существуют
    add_permission, created = Permission.objects.get_or_create(
        codename='create_task',
        content_type=content_type,
        defaults={'name': 'Can create task'}
    )

    edit_permission, created = Permission.objects.get_or_create(
        codename='edit_task',
        content_type=content_type,
        defaults={'name': 'Can edit task'}
    )

    view_permission, created = Permission.objects.get_or_create(
        codename='view_task',
        content_type=content_type,
        defaults={'name': 'Can view task'}
    )

    apply_decline_permission, created = Permission.objects.get_or_create(
        codename='apply/decline_task',
        content_type=content_type,
        defaults={'name': 'Can apply/decline task'}
    )

    delete_permission, created = Permission.objects.get_or_create(
        codename='delete_task',
        content_type=content_type,
        defaults={'name': 'Can delete task'}
    )

    # Добавляем разрешения к группам
    author_group.permissions.add(add_permission, edit_permission, view_permission, delete_permission)
    worker_group.permissions.add(view_permission, apply_decline_permission)
    admin_group.permissions.add(add_permission, edit_permission, view_permission, apply_decline_permission,
                                delete_permission)