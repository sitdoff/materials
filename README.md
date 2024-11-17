# Каталог

API каталога материалов с древовидной структурой категорий и возможностью загрузки материалов из xlsx-файлов.

## Стэк

-   **Фреймворк:** Django, Django Rest Framework
-   **База данных:** PostgreSQL
-   **Обработка задач:** Celery
-   **Брокер сообщений:** Redis
-   **HTTP-сервер:** Gunicorn
-   **Тестирование:** Pytest
-   **Контейнеризация:** Docker, Docker Compose

## Развертывание

### Docker

1. Клонируем репозиторий.

```bash
git clone https://github.com/sitdoff/materials.git
```

2. Переходим в папку проекта

```bash
cd materials
```

3. Создаем `.env`-файл с переменными окружения.

```bash
cat .env_example > .env
```

4. Запускаем сборку и запуск контейнеров

```bash

docker compose \
      -f compose/app.yaml \
      -f compose/storages.yaml \
      -f compose/celery.yaml \
      --env-file .env up -d --build

# Или используем команду make app, если пользуетесь утилитой make.
```

5. Приложение по умолчанию настроено на запуск для демонстрации. При запуске контейнера будет
   применены миграции, заполнены данные категорий и загружен суперпользователь с данными `admin:admin`.

    Приложение будет доступно по адресу http://localhost:8000/

## Endpoints

Перечень эндпоинтов находятся в разворачиваемых списках.

<details>
<summary>Материалы</summary>

---

-   #### Получить список материалов

    Method: GET

    **/api/v1/catalog/materials/list**

---

-   #### Создать новый материал

    Method: POST

    **/api/v1/catalog/materials/list**

    Пример тела запроса:

    ```json
    {
        "title": "Материал 5",
        "code": "123",
        "price": "321.00",
        "category": 1
    }
    ```

---

-   #### Получить конкретный материал используя ID

    Method: GET

    **/api/v1/catalog/materials/id/{id}**

---

-   #### Получить конкретный материал используя code

    Method: GET

    **/api/v1/catalog/materials/code/{code}**

---

-   #### Обновить данные материала используя ID

    Method: PUT

    **/api/v1/catalog/materials/id/{id}**

    Пример тела запроса:

    ```json
    {
        "title": "Обновленный материал",
        "code": "new_code",
        "price": "321.00",
        "category": 2
    }
    ```

---

-   #### Обновить данные материала используя code

    Method: PUT

    **/api/v1/catalog/materials/code/{code}**

    Пример тела запроса:

    ```json
    {
        "title": "Обновленный материал",
        "code": "new_code",
        "price": "321.00",
        "category": 2
    }
    ```

---

-   #### Удалить материал

    Method: DELETE

    **/api/v1/catalog/materials/delete/3**

---

</details>

<details>
<summary>Категории</summary>

---

-   #### Получить плоских список категорий

    Method: GET

    **/api/v1/catalog/categories/list**

---

-   #### Получить дерево категорий с материалами

    Method: GET

    **/api/v1/catalog/categories/tree**

---

-   #### Получить данные конкретной категории используя ID

    Method: GET

    **/api/v1/catalog/categories/id/{id}**

---

-   #### Создать новую категорию

    Method: POST

    **/api/v1/catalog/categories/list**

    Пример тела запроса

    ```json
    {
        "title": "New category",
        "parent": 2
    }
    ```

---

-   #### Обновить данные конкретной категории

    Method: PUT

    **/api/v1/catalog/categories/id/{id}**

    Пример тела запроса

    ```json
    {
        "title": "Детали весьма нестандартные"
    }
    ```

---

-   #### Удалить категорию

    Method: DELETE

    **/api/v1/catalog/categories/delete/{id}**

---

</details>

<details>
<summary>Работа с файлами</summary>

---

-   #### Загрузить файл с данными

    Method: POST

    **/api/v1/catalog/documents/upload**

    Загрузка должна выполняется с помощью form-data.

    file - загружаемый файл

    title - имя файла которое будет использоваться для записи в базе данных

---

-   #### Проверить статус обработки файла по его ID

    Method: GET

    **/api/v1/catalog/documents/status/{id}**

---

</details>
