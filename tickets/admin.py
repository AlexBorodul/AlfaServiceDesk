from django.contrib import admin
from .models import (
    Office, CategoryType, Employee, Task,
    ActionType, Action, Commentary,
    Attachment, Feedback, TimeLog
)

admin.site.register(Office)
admin.site.register(CategoryType)
admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(ActionType)
admin.site.register(Action)
admin.site.register(Commentary)
admin.site.register(Attachment)
admin.site.register(Feedback)
admin.site.register(TimeLog)
