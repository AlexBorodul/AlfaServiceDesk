from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Task
from .notifications.email_service import EmailNotificationService
from .change_tracker import TaskChangeTracker


@receiver(pre_save, sender=Task)
def task_pre_save(sender, instance: Task, **kwargs):
    if not instance.pk:
        return

    old_task = Task.objects.get(pk=instance.pk)
    instance._old_task = old_task

@receiver(post_save, sender=Task)
def task_worker_assigned(sender, instance: Task, created, **kwargs):
    if created:
        return

    old_task = getattr(instance, '_old_task', None)
    if not old_task:
        return

    if old_task.worker != instance.worker and instance.worker:
        EmailNotificationService.send(
            subject=f'Вам назначена заявка №{instance.pk}',
            message=(
                f'Заголовок: {instance.title}\n\n'
                f'Описание:\n{instance.problem}\n\n'
                f'Приоритет: {instance.get_priority_display()}'
            ),
            recipient=instance.worker.email
        )

@receiver(post_save, sender=Task)
def task_changed_notify(sender, instance: Task, created, **kwargs):
    if created:
        return

    old_task = getattr(instance, '_old_task', None)
    if not old_task:
        return

    tracker = TaskChangeTracker(old_task, instance)
    changes = tracker.get_changes()

    if not changes:
        return

    message = (
        f'В заявке №{instance.pk} были внесены изменения:\n\n'
        + '\n'.join(changes)
    )

    # Исполнитель
    if instance.worker:
        EmailNotificationService.send(
            subject=f'Изменения в заявке №{instance.pk}',
            message=message,
            recipient=instance.worker.email
        )

    # Автор
    if instance.author:
        EmailNotificationService.send(
            subject=f'Изменения в вашей заявке №{instance.pk}',
            message=message,
            recipient=instance.author.email
        )

@receiver(post_save, sender=Task)
def task_created_notify(sender, instance: Task, created, **kwargs):
    if not created:
        return

    if not instance.worker:
        return

    EmailNotificationService.send(
        subject=f'Вам назначена новая заявка №{instance.pk}',
        message=(
            f'Заголовок: {instance.title}\n\n'
            f'Описание проблемы:\n{instance.problem}\n\n'
            f'Приоритет: {instance.get_priority_display()}\n'
            f'Офис: {instance.office}'
        ),
        recipient=instance.worker.email
    )