from django import forms
from django.core.validators import EmailValidator
from django.forms import ModelForm
from tickets.models import Task, Employee

EMAIL_ADDRESS_MAX_LENGTH = 256

class TaskForm(ModelForm):
    files = forms.FileField(required = None)
    worker = forms.ModelChoiceField(
        queryset = Employee.objects.filter(status = 'FREE'),
        label = "Исполнитель"
    )
    class Meta:
        model = Task
        fields = ["status", "problem", "priority", "title", "category"] 


class SendEmailForm(forms.Form):
    repicient = forms.EmailField(
        max_length = EMAIL_ADDRESS_MAX_LENGTH,
        validators=[EmailValidator]
    )
    mail_theme = forms.CharField(
        max_length = 100
    )
    text = forms.CharField()
    files = forms.FileField(required = False)

class FeedbackForm(forms.Form):
    FEEDBACK_RATING = [(str(i), i) for i in range(1, 6)]
    rating = forms.ChoiceField(choices=FEEDBACK_RATING)
    feedback = forms.CharField()

