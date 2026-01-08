from django import forms
from django.core.validators import EmailValidator
from django.forms import ModelForm
from tickets.models import Task, Employee, CategoryType, Commentary
from django.core.validators import FileExtensionValidator

EMAIL_ADDRESS_MAX_LENGTH = 256


# Кастомный виджет для множественной загрузки файлов
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class TaskForm(forms.ModelForm):
    file = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt', 'zip', 'rar']
        )],
        label="Прикрепленный файл"
    )

    class Meta:
        model = Task
        fields = ["title", "problem", "priority", "category", "office", "worker", "status"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Краткое описание проблемы"
            }),
            "problem": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Подробное описание проблемы..."
            }),
            "priority": forms.Select(attrs={
                "class": "form-control"
            }),
            "status": forms.Select(attrs={
                "class": "form-control"
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "office": forms.Select(attrs={
                "class": "form-control"
            }),
            "worker": forms.Select(attrs={
                "class": "form-control"
            }),
        }
        labels = {
            'title': 'Тема заявки',
            'problem': 'Описание проблемы',
            'category': 'Категория',
            'priority': 'Приоритет',
            'office': 'Офис',
            'worker': 'Исполнитель',
            'status': 'Статус',
        }

    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настраиваем queryset для поля worker
        self.fields['worker'].queryset = Employee.objects.all().order_by('first_name')

        # Настраиваем queryset для поля category
        self.fields['category'].queryset = CategoryType.objects.all()

        # Делаем поле worker необязательным
        self.fields['worker'].required = False
        self.fields['worker'].empty_label = "Автоматический выбор"
        self.fields['worker'].help_text = "Оставьте пустым для автоматического назначения" '''

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and hasattr(self.user, 'employee'):
            employee = self.user.employee
            # Автоматически выбираем офис сотрудника
            if employee and employee.office:
                self.fields['office'].initial = employee.office


class SendEmailForm(forms.Form):
    recipient = forms.EmailField(
        max_length=EMAIL_ADDRESS_MAX_LENGTH,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
        }),
        label="Получатель"
    )
    mail_theme = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Тема письма'
        }),
        label="Тема"
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Текст письма...'
        }),
        label="Текст письма"
    )
    files = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'multiple': True
        }),
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt', 'zip']
        )],
        label="Прикрепленные файлы"
    )


class FeedbackForm(forms.Form):
    FEEDBACK_RATING = [(str(i), f"{i} звезд{'а' if i == 1 else 'ы' if i in [2, 3, 4] else ''}") for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=FEEDBACK_RATING,
        widget=forms.RadioSelect(),
        label="Оценка"
    )
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Ваш комментарий...'
        }),
        label="Комментарий",
        required=False
    )


class CommentForm(forms.ModelForm):
    """Форма для добавления комментариев"""

    class Meta:
        model = Commentary
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите комментарий...'
            }),
        }
        labels = {
            'text': 'Комментарий',
        }


class TaskFilterForm(forms.Form):
    """Форма для фильтрации заявок"""
    STATUS_CHOICES = [('', 'Все статусы')] + list(Task.STATUS_CHOICES)
    PRIORITY_CHOICES = [('', 'Все приоритеты')] + list(Task.PRIORITY_CHOICES)

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=CategoryType.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Все категории"
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по ID, названию или описанию...'
        })
    )