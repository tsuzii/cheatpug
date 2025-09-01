FROM python:3.13-slim

# Устанавливаем системные зависимости для сборки Python пакетов
RUN apt-get update && apt-get install -y curl build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Рабочая директория
WORKDIR /app

# Копируем файлы для Poetry сначала (оптимизация кэша)
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости без создания виртуального окружения
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

# Копируем остальной код проекта
COPY . /app

# Переменные окружения для токенов
ENV TELEGRAM_BOT_TOKEN=""
ENV DEEPSEEK_TOKEN=""

# Команда запуска бота
CMD ["python", "main.py"]
