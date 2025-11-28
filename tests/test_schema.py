from django.test import TestCase
from tickets.forms import TaskForm
from tickets.models import CategoryType

class TaskFormTestCase(TestCase):
    def setUp(self):
        self.category = CategoryType.objects.create(name = 'Test_Category')

    def test_from_valid_data(self):
        valid_data = {
            "title": "Title for Task",
            "status": 'waiting',
            "problem": "Base problem",
            "priority": 'value1',
            "category": self.category
        }
        task = TaskForm(data = valid_data)
        self.assertTrue(task.is_valid())
    
    def test_from_invalid_data(self):
        invalid_data = {
        "status": 'invalid_status',
        "problem": "Same problem",
        "priority": 'invalid_value'
    }
        task = TaskForm(data = invalid_data)
        self.assertFalse(task.is_valid())