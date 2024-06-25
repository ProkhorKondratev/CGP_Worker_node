# Используем официальный образ Python 3.12 slim
FROM python:3.12-slim-bookworm

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN pip install --no-cache-dir poetry

# Создаем рабочую директорию для приложения
WORKDIR /app

# Копируем файлы конфигурации poetry
COPY poetry.lock pyproject.toml /app/

# Устанавливаем зависимости проекта через poetry без создания виртуального окружения
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Копируем исходный код приложения
COPY ./app /app

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Открываем порт для внешних запросов
EXPOSE 8000

# Запускаем приложение FastAPI с использованием Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
