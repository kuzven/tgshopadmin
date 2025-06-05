FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта
COPY . .

# Собираем статические файлы
RUN python manage.py collectstatic --noinput

# Запускаем Gunicorn
CMD ["gunicorn", "tgshopadmin.wsgi.application", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "--timeout", "60"]