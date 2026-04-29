# Контрольная работа №4 Суринов Артём ЭФБО-03-24

## Структура проекта

├── task_9_1/   
├── task_10_1/  
├── task_10_2/  
├── task_11_1/  
├── task_11_2/  
├── requirements.txt
└── .gitignore


---

## Установка

### 1) Клонирование репозитория
```bash
git clone <url-репозитория>
cd Surinov_efbo-03-24_trsp_kr4
```

### 2) Виртуальное окружение
**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3) Установка зависимостей
```bash
pip install -r requirements.txt
```

---

## Запуск приложений (по заданиям)

> Каждый модуль запускается отдельно на своём порту.  
> Документация Swagger доступна по адресу: `http://127.0.0.1:<порт>/docs`

### Задание 9.1 — Alembic миграции + Product API (порт 8000)

1) Применить миграции:
```bash
cd task_9_1
alembic upgrade head
cd ..
```

2) Запустить приложение:
```bash
uvicorn task_9_1.main:app --reload --port 8000
```

Swagger:
- http://127.0.0.1:8000/docs

---

### Задание 10.1 — Пользовательская обработка ошибок (порт 8001)

Запуск:
```bash
uvicorn task_10_1.main:app --reload --port 8001
```

Swagger:
- http://127.0.0.1:8001/docs

---

### Задание 10.2 — Валидация данных (порт 8002)

Запуск:
```bash
uvicorn task_10_2.main:app --reload --port 8002
```

Swagger:
- http://127.0.0.1:8002/docs

---

### Задание 11.1 — Приложение для тестов (порт 8003)

Запуск:
```bash
uvicorn task_11_1.main:app --reload --port 8003
```

Swagger:
- http://127.0.0.1:8003/docs

---

## Проверка основной функциональности

### Задание 9.1 — Product API + миграции

Открыть:
- http://127.0.0.1:8000/docs

Проверить эндпоинты:
- `GET /products` — получить список товаров
- `POST /products` — создать товар

Проверка истории миграций:
```bash
cd task_9_1
alembic history
cd ..
```

---

### Задание 10.1 — Обработка ошибок

Открыть:
- http://127.0.0.1:8001/docs

Ключевые сценарии:
- `GET /products/1` — товар найден (200)
- `GET /products/999` — `ProductNotFoundException` (404)
- `PUT /products/1` с `price=-100` — `InvalidProductDataException` (422)
- `PUT /products/1` с `title="A"` — `InvalidProductDataException` (422)

---

### Задание 10.2 — Валидация пользователей

Открыть:
- http://127.0.0.1:8002/docs

Ключевые сценарии:
- `POST /users` с валидными данными — успех (200)
- `POST /users` с `age=15` — ошибка валидации (422)
- `POST /users` с `email="bad"` — ошибка валидации (422)
- `POST /users` с `password="short"` — ошибка валидации (422)
- `POST /users` без `phone` — поле `phone="Unknown"` по умолчанию

---

### Задание 11.1 — Основные сценарии API (для модульных тестов)

Открыть:
- http://127.0.0.1:8003/docs

Ключевые сценарии:
- `POST /register` — регистрация пользователя
- `GET /users/{id}` — получение пользователя
- `DELETE /users/{id}` — удаление пользователя
- `GET /users` — список всех пользователей

---

### Задание 11.2 — Асинхронные тесты (без запуска сервера)

Суть:
- тесты используют `Faker`, `httpx.AsyncClient` и `ASGITransport`
- сервер **не нужно** запускать (всё работает через ASGI-приложение напрямую)

---

## Тестирование (ключевые сценарии)

### Задание 11.1 — модульные тесты
```bash
python -m pytest task_11_1/test_main.py -v
```

### Задание 11.2 — асинхронные тесты
```bash
python -m pytest task_11_2/test_main_async.py -v
```

### Запуск всех тестов
```bash
python -m pytest task_11_1/ task_11_2/ -v
```

---

## Примечания
- Если порт занят — измените `--port` на свободный.
- Для удобства проверки используйте Swagger UI (`/docs`) для каждого задания.
