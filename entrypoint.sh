#!/bin/bash
# Устанавливаем строгий режим
set -e

# Ожидание доступности базы данных
./wait-for-it.sh postgres_db:5432 -- echo "PostgreSQL is ready"

# Применение миграций, если это необходимо
# python manage.py makemigrations && python manage.py migrate

# Запуск вашего Django приложения
exec "$@"
