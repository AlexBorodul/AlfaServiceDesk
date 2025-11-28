import re
from django import forms
from django.forms import ModelForm
from tickets.models import Task
from django.core.validators import EmailValidator

def is_valid_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*d)[A-Za-zd]{8,}$'
    return bool(re.match(pattern, password))

CATEGORY_CHOICES = [("category.name1", "category.description1")]

class TaskForm(ModelForm):
    author = forms.CharField(max_length = 60)
    worker = forms.CharField(max_length = 60)
    category = forms.ChoiceField(choices = CATEGORY_CHOICES)
    office = forms.CharField(max_length=100)

    class Meta:
        model = Task
        fields = ["__all__"] 
        exclude = ['created_at', "updated_at", "actual_cost", "worker", "author", "office"]

class IdentificationForm(forms.Form):
    email = forms.EmailField(
        label = 'Email',
        widget = forms.EmailInput(attrs={'placeholder': 'Введите ваш Email'}),
        validators=[EmailValidator()]
    )
    password = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(attrs={'placeholder': 'Введите ваш пароль'}),
        validators = [is_valid_password()]
    )

    def is_valid_password(password):
        pattern = r'^(?=.*[A-Z])(?=.*d)[A-Za-zd]{8,}$'
        return bool(re.match(pattern, password))
    

