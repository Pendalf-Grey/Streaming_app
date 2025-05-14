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
RUN pip install --upgrade pip && \
    pip install poetry==1.8.5 && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Для запуска с помощью FastAPI
CMD ["uvicorn", "streaming_app_authorization.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
