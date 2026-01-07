from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from tickets.models import Task

def create_group(apps, schema_editor):
    content_type = ContentType.objects.get_for_model(Task)

    author_group, _ = Group.objects.get_or_create(name="Author")
    worker_group, _ = Group.objects.get_or_create(name="Worker")
    admin_group, _ = Group.objects.get_or_create(name="Admin")

    add_permission, _ = Permission.objects.get_or_create(
        codename='create_task', 
        name='can create task', 
        content_type=content_type
    )
    edit_permission, _ = Permission.objects.get_or_create(
        codename='edit_task', 
        name='can edit task', 
        content_type=content_type
    )
    view_permission, _ = Permission.objects.get_or_create(
        codename='view_task', 
        name='can view task', 
        content_type=content_type
    )
    apply_decline_permission, _ = Permission.objects.get_or_create(
        codename='apply_decline_task', 
        name='can apply/decline task', 
        content_type=content_type
    )
    delete_permission, _ = Permission.objects.get_or_create(
        codename='delete_task', 
        name='can delete task', 
        content_type=content_type
    )

    author_group.permissions.set([add_permission, edit_permission, view_permission, delete_permission])
    worker_group.permissions.set([view_permission, apply_decline_permission])
    admin_group.permissions.set([add_permission, edit_permission, view_permission, apply_decline_permission, delete_permission])
