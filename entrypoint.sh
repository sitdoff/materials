#!/bin/bash
# Устанавливаем строгий режим
set -e

# Ожидание доступности базы данных
./wait-for-it.sh postgres_db:5432 -- echo "PostgreSQL is ready"

# Создание и применение миграций, если это необходимо
python manage.py makemigrations && python manage.py migrate

# Заполняем базу начальными данными
python manage.py loaddata dump.json

# Вносим в базу суперюзера
python manage.py loaddata superuser.json

# Собираем статику
python manage.py collectstatic --noinput


# Запуск вашего Django приложения
exec "$@"
