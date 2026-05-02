# FastAPI Library Project

Цей репозиторій містить серію лабораторних робіт з розробки сучасних API на Python. Проєкт еволюціонує від простого скрипта до повноцінної мікросервісної архітектури.


- **Lab 1: Основи FastAPI** — Знайомство з фреймворком, маршрутизація, Pydantic моделі та перші CRUD операції.
- **Lab 2: PostgreSQL & SQLAlchemy** — Перехід на реляційну БД, робота з ORM та реалізація `Limit-Offset` пагінації.
- **Lab 3: Cursor Pagination** — Оптимізація пагінації для великих обсягів даних за допомогою курсорів.
- **Lab 4: MongoDB Integration** — Додавання підтримки NoSQL бази даних для гнучкого зберігання документів.
- **Lab 5: Advanced API Logic** — Робота з файлами, складними запитами та бізнес-процесами.
- **Lab 6: Authentication & Security** — Реалізація JWT, OAuth2 та розмежування прав доступу (Scopes).
- **Lab 7: Rate Limiter** — Захист API від перевантажень та спаму.
- **Lab 8: Mocking** — Створення Mock-сервісів для тестування та інтеграцій.
- **Lab 9: Testing** — Покриття коду юніт-тестами (Pytest) та інтеграційне тестування.

---

## Технології:

- **Backend:** Python 3.12, FastAPI
- **Data:** SQLAlchemy (PostgreSQL), Beanie (MongoDB)
- **Infrastructure:** Docker, Docker Compose
- **Testing:** Pytest, HTTPX

---

## Швидкий старт (Docker):

Найпростіший спосіб запустити будь-який етап проєкту:
```bash
# Клонування репозиторію
git clone [https://github.com/yavorskii/fastapi-labs.git](https://github.com/yavorskii/fastapi-labs.git)

# Запуск стеку (API + DB)
docker-compose up --build
