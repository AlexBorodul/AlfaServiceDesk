class TaskChangeTracker:
    FIELDS_VERBOSE = {
        'status': 'Статус',
        'priority': 'Приоритет',
        'category': 'Категория',
        'office': 'Офис',
        'worker': 'Исполнитель',
        'problem': 'Описание проблемы',
    }

    def __init__(self, old, new):
        self.old = old
        self.new = new

    def get_changes(self):
        changes = []

        for field, label in self.FIELDS_VERBOSE.items():
            old_value = getattr(self.old, field)
            new_value = getattr(self.new, field)

            if old_value != new_value:
                changes.append(
                    f'{label}: "{old_value}" → "{new_value}"'
                )

        return changes
