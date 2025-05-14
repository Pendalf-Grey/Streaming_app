# Запуск контейнеров
run:
	docker-compose up

# Остановка контейнеров
stop:
	docker-compose down

# Установка зависимостей
install:
	poetry install

# Создание миграций (если используете Alembic для SQL)
migrations:
	poetry run alembic revision --autogenerate -m "Migration message"

# Применение миграций (если используете Alembic для SQL)
migrate:
	poetry run alembic upgrade head

# Создание суперпользователя (если необходимо)
superuser:
	poetry run python -c "from your_module import create_superuser; create_superuser()"

# Запуск оболочки
shell:
	poetry run python

# Загрузка данных в MongoDB
load_data:
	poetry run python -c "from your_module import load_fixtures; load_fixtures()"

# Ожидание готовности MongoDB (дополнительно)
wait-for-mongo:
	@echo "Waiting for MongoDB to be ready..."
	@until nc -z mongo 27017; do sleep 1; done
	@echo "MongoDB is ready!"

# Объединенная команда для установки и запуска
start:
	make install
	make wait-for-mongo
	make run



# Проект --- N1_Prompts
# run:
# 	docker compose up
# install:
# 	make migrations
# 	make migrate
# 	make superuser
# migrations:
# 	python manage.py makemigrations
# migrate:
# 	python manage.py migrate
# superuser:
# 	python manage.py createsuperuser
# shell:
# 	python manage.py shell
# fixtures:
# 	make load_data
# load_data:
# 	python manage.py loaddata fixtures/models.json fixtures/purposes.json