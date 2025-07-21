# QRkot_spreadseets

## Оглавление

- [Автор](#автор)  
- [Используемые технологии](#используемые-технологии)  
- [Описание проекта](#описание-проекта)  
- [Установка и запуск](#установка-и-запуск)  
- [Примеры использования](#примеры-использования)  

---

## Используемые технологии

- Python 3.9+
- FastAPI (REST API)
- SQLAlchemy (асинхронный ORM)
- PostgreSQL (база данных)
- Alembic (миграции)
- Pydantic (валидация данных)
- OAuth2 и JWT (аутентификация и авторизация)
- Pytest (тестирование)
- Uvicorn 0.17.6
- Google API


---

## Описание проекта

QRKot — это приложение для благотворительного фонда поддержки котиков.
Фонд собирает пожертвования на различные целевые проекты: медицинское обслуживание, обустройство кошачьих колоний, кормление бездомных кошек и другие задачи, связанные с поддержкой кошачьей популяции.

---

## Установка и запуск

1. Клонируйте репозиторий и перейдите в папку проекта:  
   ```bash
   git clone https://github.com/AnastasiaDeka/QRkot_spreadsheets.git
   cd QRkot_spreadsheets
   ```


Создайте и активируйте виртуальное окружение:

2. Для Linux/macOS:
   ```bash
    python -m venv venv
    source venv/bin/activate
   ```


   Для Windows:
   ```bash
    python -m venv venv
    venv\Scripts\activate
   ```
3. Обновите pip:
   ```bash
    python -m pip install --upgrade pip
   ```
4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

# Примеры использования

   Создайте файл .env или измените параметры app.core.config

    ```
    touch .env
    ```
   Заполните файл .env:

    ```
    DATABASE_URL=
    SECRET=
    APP_TITLE=
    FIRST_SUPERUSER_EMAIL=
    FIRST_SUPERUSER_PASSWORD=
    # Данные вашего сервисного аккаунта
    TYPE=
    PROJECT_ID=
    PRIVATE_KEY_ID=
    PRIVATE_KEY=
    CLIENT_EMAIL=
    CLIENT_ID=
    AUTH_URI=
    TOKEN_URI=
    AUTH_PROVIDER_X509_CERT_URL=
    CLIENT_X509_CERT_URL=
    EMAIL=
    ```
   Запустить проект:

    ```
    uvicorn app.main:app --reload
    ```
   Проект будет доступен по: http://127.0.0.0:8000/ .

    Documentation is available at: 
* Swagger: http://127.0.0.0:8000/docs
* ReDoc: http://127.0.0.0:8000/redoc

---

## Автор

- [Декапольцева Анастасия](https://github.com/AnastasiaDeka)