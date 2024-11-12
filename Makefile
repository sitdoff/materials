DC = docker compose
APP_FILE = compose/app.yaml
APP_CONTAINER = main-app
STORAGES_FILE = compose/storages.yaml
EXEC = docker exec -it
DB_CONTAINER = postgres_db
LOGS = docker logs
ENV = --env-file .env
MANAGE_PY = python manage.py

.PHONY: storages
storages: ## Поднять хранилища данных
		${DC} -f ${STORAGES_FILE} ${ENV} up -d

.PHONY: storages-down
storages-down: ## Остановить хранилища данных
		${DC} -f ${STORAGES_FILE} down

.PHONY: postgres
postgres: ## Поднять только Postgres
		${EXEC} ${DB_CONTAINER} psql -U postgres

.PHONY: storages-logs
storages-logs: ## Показать логи Postgres
		${LOGS} ${DB_CONTAINER} -f

.PHONY: app
app: ## Запуск приложения в контейнере
		${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV} up -d

.PHONY: app-rebuild
app-rebuild: ## Запуск приложения в контейнере с ребилдом контейнера
		${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV} up -d --build

.PHONY: app-logs
app-logs: ## Показать логи приложения в контейнере
		${LOGS} ${APP_CONTAINER} -f

.PHONY: app-down
app-down: ## Остановить приложение в контейнере
		${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: migrations
migrations: ## Создание миграций в контейнере
		${EXEC} ${APP_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: migrate
migrate: ## Запуск миграции в контейнере
		${EXEC} ${APP_CONTAINER} ${MANAGE_PY} migrate

.PHONY: superuser
superuser: ## Создать суперюзера в контейнере
		${EXEC} ${APP_CONTAINER} ${MANAGE_PY} createsuperuser

.PHONY: collectstatic
collectstatic: ## Собрать статические файлы в контейнере
		${EXEC} ${APP_CONTAINER} ${MANAGE_PY} collectstatic
