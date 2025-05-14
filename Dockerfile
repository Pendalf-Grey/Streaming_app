# Используемый ЯП и версия
FROM python:3.10

# Логи будут отображаться в Docker мгновенно
ENV PYTHONUNBUFFERED=1

# Даём имя рабочей директории в Docker-контейнере
WORKDIR /web_fastapi

# Просто копируем файлы (COPY) в рабочую директорию
COPY pyproject.toml poetry.lock Makefile docker-compose.yml ./

# Копируем файл (COPY) внутрь создаваемой директории streaming_app_authorization,
# которая расположена внутри директории web_fastapi
COPY streaming_app_authorization/ ./streaming_app_authorization/

# Устанавливаем зависимости через Poetry
RUN pip install --upgrade pip --progress-bar off && \
    pip install --no-cache-dir poetry --progress-bar off && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Для запуска с помощью FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
