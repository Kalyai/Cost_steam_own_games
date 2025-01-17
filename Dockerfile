# Используем базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Устанавливаем переменные окружения для Django
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=myproject.settings

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "myproject/manage.py", "runserver", "0.0.0.0:8000"]
