from django import forms


class TaskForm(forms.Form):
    status =  forms.CharField(
        max_length = 30,
        widget = forms.Select(
            ('value1', 'value1'),
            ('value2', 'value2'),
            ('value3', 'value3'),
            ('value4', 'value4'),
        )
    )
    problem = forms.CharField()
    priority = forms.CharField(
        widget = forms.Select(
            ('value1', 'value1'),
            ('value2', 'value2'),
            ('value3', 'value3'),
            ('value4', 'value4'),
        )
    ),


