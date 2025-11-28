from django.test import TestCase
from tickets.schemas import TaskForm

class TaskFormTestCase(TestCase):
    def test_from_valid_data(self):
        data = {
            "status": 'value1',
            "problem": "Base problem",
            "priority": 'value1'
        }
        task = TaskForm(data = data)
        self.assertTrue(task.is_valid())
    
    def test_from_invalid_data(self):
        data = {
        "status": 'invalid_status',
        "problem": "Same problem",
        "priority": 'invalid_value'
    }
        task = TaskForm(data = data)
        self.assertFalse(task.is_valid())