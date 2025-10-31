# Dockerfile
FROM python:3.14-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установим Flower явно
# RUN pip install flower

COPY . .

CMD ["gunicorn", "service_desk.wsgi:application", "--bind", "0.0.0.0:8000"]
