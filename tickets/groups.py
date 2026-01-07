from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from tickets.models import Task


def create_group(apps, schema_editor):

    content_type = ContentType.objects.get_for_model(Task)

    author_group = Group.objects.create(name="Author")
    worker_group = Group.objects.create(name="Worker")
    admin_group = Group.objects.create(name="Admin")

    add_permission = Permission.objects.create(codename = 'create_task', content_type=content_type)
    edit_permission = Permission.objects.create(codename = 'edit_task', content_type=content_type)
    view_permission = Permission.objects.create(codename = 'view_task', content_type=content_type)
    apply_decline_permission = Permission.objects.create(codename = 'apply/decline_task', content_type=content_type)
    delete_permission = Permission.objects.create(codename = 'delete_task', content_type=content_type)

    author_group.permissions.add(add_permission, edit_permission, view_permission, delete_permission)
    worker_group.permissions.add(view_permission, apply_decline_permission)
    admin_group.permissions.add(add_permission, edit_permission, view_permission, apply_decline_permission, delete_permission)

