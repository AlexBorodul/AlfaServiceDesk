from django.db.models.query import QuerySet
from tickets.models import Employee, Task

class WorkerController:
    """Занимается выбором исполнителя задачи."""
    @classmethod
    def auto_select_worker(cls, task: Task) -> None:
        """Автоматический выбор исполнителя."""
        workers = Employee.objects.filter(specialization = task.category, office=task.office).all()
        emptiest_worker = min(workers, key = WorkerController.get_worker_tasks)
        task.worker = emptiest_worker
    @classmethod
    def change_to_main_worker(cls, task: Task) -> None:
        """Смена исполнителя на главного в офисе"""
        task.worker = task.worker.parent
    @classmethod
    def get_subordinates(cls, main_worker: Employee) -> QuerySet[Employee]:
        """Возвращает список подчинённых"""
        return Employee.objects.filter(parent = main_worker)

    @classmethod
    def get_worker_tasks(cls, worker: Employee) -> int:
        """Возвращает список заявок у исполнителя."""
        return len(Task.objects.filter(worker = worker))