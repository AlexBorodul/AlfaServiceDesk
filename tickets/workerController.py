from django.db.models.query import QuerySet
from tickets.models import Employee

class WorkerController:
    """Занимается выбором исполнителя задачи."""
    def __init__(self, workers: QuerySet) -> None:
        """Инициализация."""
        self.workers = workers
    
    def auto_select_worker(self) -> Employee:
        """Автоматический выбор исполнителя."""
        pass

    def change_worker(self) -> Employee:
        """Смена исполнителя"""
        pass

    def get_subordinates(self, main_worker) -> list[Employee]:
        """Возвращает список подчинённых"""
        pass