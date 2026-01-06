from django.db.models import Q
from tickets.models import Employee, Task, Office
from datetime import datetime


class WorkerController:
    """Контроллер для работы с исполнителями задач."""

    @classmethod
    def auto_select_worker(cls, task: Task) -> Employee:
        """Автоматический выбор исполнителя на основе критериев."""
        # 1. Ищем свободных сотрудников с нужной специализацией в том же офисе
        worker = Employee.objects.filter(
            Q(status='FREE') | Q(status=None),
            specialization=task.category,
            office=task.office
        ).first()

        # 2. Если не нашли, ищем в том же офисе без учета специализации
        if not worker:
            worker = Employee.objects.filter(
                Q(status='FREE') | Q(status=None),
                office=task.office,
                role='worker'  # предполагаем, что есть поле role в модели
            ).first()

        # 3. Если все еще не нашли, ищем любого свободного исполнителя
        if not worker:
            worker = Employee.objects.filter(
                Q(status='FREE') | Q(status=None),
                role='worker'
            ).first()

        # 4. Если исполнитель найден - обновляем статус
        if worker:
            task.worker = worker
            worker.status = 'BUSY'
            worker.save()
        else:
            # Если исполнителей нет - можно назначить руководителю офиса
            if task.office and task.office.main_worker:
                task.worker = task.office.main_worker

        return task

    @classmethod
    def change_worker(cls, task: Task, new_worker_id: int) -> Task:
        """Смена исполнителя задачи."""
        old_worker = task.worker

        # Освобождаем старого исполнителя
        if old_worker:
            old_worker.status = 'FREE'
            old_worker.save()

        # Назначаем нового
        new_worker = Employee.objects.get(pk=new_worker_id)
        task.worker = new_worker
        new_worker.status = 'BUSY'
        new_worker.save()

        return task

    @classmethod
    def get_available_workers(cls, task: Task = None) -> list:
        """Получение списка доступных исполнителей."""
        base_query = Employee.objects.filter(role='worker')

        if task:
            # Приоритет: специализация + офис
            workers = base_query.filter(
                Q(status='FREE') | Q(status=None),
                specialization=task.category,
                office=task.office
            )
            if not workers.exists():
                workers = base_query.filter(
                    Q(status='FREE') | Q(status=None),
                    office=task.office
                )
        else:
            workers = base_query.filter(Q(status='FREE') | Q(status=None))

        return list(workers)

    @classmethod
    def get_subordinates(cls, manager: Employee) -> list[Employee]:
        """Возвращает список подчинённых (по полю parent в модели Employee)."""
        return list(Employee.objects.filter(parent=manager))

    @classmethod
    def free_worker(cls, worker: Employee):
        """Освобождение исполнителя после завершения задачи."""
        worker.status = 'FREE'

        # Проверяем, нет ли у него других активных задач
        active_tasks = Task.objects.filter(
            worker=worker
        ).exclude(status__in=['done', 'rejected'])

        if active_tasks.exists():
            worker.status = 'BUSY'

        worker.save()
        return worker

    @classmethod
    def get_worker_stats(cls, worker: Employee) -> dict:
        """Получение статистики по исполнителю."""
        total_tasks = Task.objects.filter(worker=worker).count()
        completed_tasks = Task.objects.filter(worker=worker, status='done').count()
        avg_completion_time = None

        if completed_tasks > 0:
            return {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
                'avg_completion_time': avg_completion_time,
            }