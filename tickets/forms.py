from django.forms import ModelForm
from tickets.models import Task

class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ["status", "problem", "priority", "title", "category"] 


    

