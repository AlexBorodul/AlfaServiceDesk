from django.db.models.query import QuerySet
from tickets.models import Employee, Task

class WorkerController:
    """Занимается выбором исполнителя задачи."""
    @classmethod
    def auto_select_worker(cls, task: Task) -> Employee:
        """Автоматический выбор исполнителя."""
        worker = Employee.objects.filter(status='FREE', specialization=task.category).first()
        task.worker = worker
        worker.status = 'BUSY'
        worker.save()
        return task
    @classmethod
    def change_worker(self) -> Employee:
        """Смена исполнителя"""
        pass
    @classmethod
    def get_subordinates(self, main_worker) -> list[Employee]:
        """Возвращает список подчинённых"""
        pass