from django.db.models.query import QuerySet
from tickets.models import Employee, Task

class WorkerController:
    """Занимается выбором исполнителя задачи."""
    @classmethod
    def auto_select_worker(cls, task: Task) -> Employee:
        """Автоматический выбор исполнителя."""
        workers = Employee.objects.filter(specialization = task.category, office=task.office).all()
        emptiest_worker = min(workers, key = WorkerController.get_worker_tasks)
        task.worker = emptiest_worker
        return task
    @classmethod
    def change_worker(self) -> Employee:
        """Смена исполнителя"""
        pass
    @classmethod
    def get_subordinates(self, main_worker) -> list[Employee]:
        """Возвращает список подчинённых"""
        pass

    @classmethod
    def get_worker_tasks(cls, worker: Employee):
        return len(Task.objects.filter(worker = worker))