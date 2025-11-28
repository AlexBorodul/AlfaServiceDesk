from django.test import TestCase
from tickets.forms import TaskForm, SendEmailForm, FeedbackForm
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
            "category": self.category,
            "files":  None
        }
        task_form = TaskForm(data = valid_data)
        self.assertTrue(task_form.is_valid())
    
    def test_from_invalid_data(self):
        invalid_data = {
        "status": 'invalid_status',
        "problem": "Same problem",
        "priority": 'invalid_value',
        "category": self.category,
        "files":  None
    }
        task_form = TaskForm(data = invalid_data)
        self.assertFalse(task_form.is_valid())

class SendEmailFornTestCase(TestCase):
    def test_from_valid_data(self):
        valid_data = {
            'repicient': 'test@example.com',
            'mail_theme': 'Test Theme',
            'text': 'This is a test email.',
            'files': None
        }
        mail_form = SendEmailForm(valid_data)
        self.assertTrue(mail_form.is_valid())

    def test_from_invalid_data(self):
        invalid_data = {
            "repicient": "invalid mail",
            "mail_theme": "Theme for a Mail!"
        }
        mail_form = SendEmailForm(invalid_data)
        self.assertFalse(mail_form.is_valid())

class FeedbackFormTestCase(TestCase):
    def test_from_valid_data(self):
        valid_data = {
            "rating": "1",
            "feedback": "Good!"
        }
        feedback_form = FeedbackForm(valid_data)
        self.assertTrue(feedback_form.is_valid())
    
    def test_from_invalid_data(self):
        valid_data = {
            "rating": "invalid_data",
            "feedback": "Good!"
        }
        feedback_form = FeedbackForm(valid_data)
        self.assertFalse(feedback_form.is_valid())