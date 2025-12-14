import os
import shutil


def create_project_structure():
    """Создает структуру папок и файлов для проекта"""

    # Пути
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Создаем папки
    folders = [
        'templates/includes',
        'tickets/templates/tickets',
        'static/css',
        'static/js',
        'media/attachments'
    ]

    for folder in folders:
        path = os.path.join(base_dir, folder)
        os.makedirs(path, exist_ok=True)
        print(f'Создана папка: {path}')

    # Создаем файлы (опционально, если нужно)
    # Здесь можно добавить автоматическое создание файлов

    print("Структура проекта создана успешно!")


if __name__ == "__main__":
    create_project_structure()