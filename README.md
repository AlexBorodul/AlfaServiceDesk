# 🧰 Service Desk Alfa

Система **Service Desk Alfa** — это внутренняя платформа для учёта, обработки и анализа заявок сотрудников компании.  

---

## ⚙️ Технологии

| Компонент | Используется |
|------------|--------------|
| Backend | Django |
| ORM | Django ORM |
| Асинхронные задачи | Celery |
| Брокер сообщений | Redis |
| Планировщик | Celery Beat |
| Мониторинг задач | Flower |
| БД (локально) | SQLite |
| БД (в проде) | PostgreSQL |
| Веб-сервер | Gunicorn |
| Контейнеризация | Docker / Docker Compose |
| CI/CD | GitLab CI (будет добавлен позже) |

---

## 📦 Установка и запуск (локально)


Создайте виртуальное окружение и установите зависимости
python3 -m venv venv
source venv/bin/activate     # Linux / Mac
pip install -r requirements.txt


Примените миграции
python manage.py makemigrations
python manage.py migrate

Создайте суперюзера
python manage.py createsuperuser

Заупстите сервак
python manage.py runserver

НЕБОЛЬШАЯ ПРОСЬБА
Создавайте ветки не от своего имени, а от конкретной фичи, которую будете пилить. Потом закидывайте в репу и создавайте MR - я если что буду уже кидать аппрув и мерджить

Всем 52!