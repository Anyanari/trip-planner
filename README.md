# Trip Planner - Сервис планирования поездок

Trip Planner - это веб-приложение для совместного планирования путешествий, которое позволяет пользователям создавать маршруты, предлагать места для посещения, управлять расходами и голосовать за предложения.

## Возможности

- 🗺️ Создание и управление поездками
- 👥 Приглашение участников в поездки
- 📍 Поиск и добавление мест из OpenStreetMap
- 🗳️ Голосование за предложенные места
- 💰 Управление общими расходами
- 📅 Планирование маршрутов по дням

## Технологический стек

### Backend
- **FastAPI** - веб-фреймворк для создания API
- **SQLAlchemy** - ORM для работы с базой данных
- **PostgreSQL** - основная база данных
- **Alembic** - управление миграциями БД
- **Pydantic** - валидация данных
- **JWT** - аутентификация пользователей

### Frontend
- **React 18** - библиотека для создания пользовательского интерфейса
- **TypeScript** - типизация JavaScript
- **Tailwind CSS** - фреймворк для стилизации
- **React Router** - маршрутизация в приложении
- **Axios** - HTTP клиент для API запросов

### DevOps
- **Docker** - контейнеризация
- **Docker Compose** - оркестрация контейнеров
- **PostgreSQL** - база данных в контейнере

## Структура проекта

```
trip-planner/
├── backend/                 # Backend приложение
│   ├── app/
│   │   ├── models.py       # Модели SQLAlchemy
│   │   ├── schemas.py      # Pydantic схемы
│   │   ├── main.py         # FastAPI приложение
│   │   ├── database.py     # Настройки БД
│   │   ├── config.py       # Конфигурация
│   │   └── routers/        # API роутеры
│   ├── tests/              # Тесты
│   ├── migrations/         # Миграции БД
│   ├── requirements.txt    # Зависимости Python
│   └── Dockerfile          # Docker конфигурация
├── frontend/               # Frontend приложение
│   ├── src/
│   │   ├── components/     # React компоненты
│   │   ├── pages/          # Страницы
│   │   ├── services/       # API сервисы
│   │   └── types/          # TypeScript типы
│   ├── public/             # Статические файлы
│   ├── package.json        # Зависимости Node.js
│   └── Dockerfile          # Docker конфигурация
├── database/               # Конфигурация БД
│   ├── init.sql            # Инициализация БД
│   └── Dockerfile          # Docker конфигурация
├── docker-compose.yml      # Docker Compose конфигурация
└── README.md              # Этот файл
```

## Быстрый старт

### Предварительные требования

- [Docker](https://www.docker.com/) и Docker Compose
- [Node.js](https://nodejs.org/) (версии 18 или выше)
- [Python](https://www.python.org/) (версии 3.11 или выше)

### Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd trip-planner
   ```

2. **Запустите скрипт настройки:**
   ```bash
   python setup.py
   ```

   Этот скрипт автоматически:
   - Проверит наличие необходимых инструментов
   - Настроит виртуальное окружение для Python
   - Установит все зависимости
   - Создаст файлы конфигурации
   - Запустит тесты

3. **Запустите приложение:**
   ```bash
   python setup.py start
   ```
   Или вручную:
   ```bash
   docker-compose up --build
   ```

4. **Откройте приложение в браузере:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API документация: http://localhost:8000/docs
   - База данных: http://localhost:5050 (pgAdmin)

## Ручная настройка

### Backend

1. **Создайте виртуальное окружение:**
   ```bash
   cd backend
   python -m venv venv
   ```

2. **Активируйте окружение:**
   ```bash
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Создайте файл .env:**
   ```bash
   cp .env.example .env
   ```
   Отредактируйте `.env` файл с вашими настройками.

5. **Запустите миграции:**
   ```bash
   alembic upgrade head
   ```

6. **Запустите сервер:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend

1. **Установите зависимости:**
   ```bash
   cd frontend
   npm install
   ```

2. **Запустите сервер разработки:**
   ```bash
   npm start
   ```

## Тестирование

### Backend тесты
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend тесты
```bash
cd frontend
npm test
```

## API документация

После запуска backend сервера, вы можете получить доступ к интерактивной документации API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Основные эндпоинты API

### Аутентификация
- `POST /api/auth/register` - Регистрация пользователя
- `POST /api/auth/token` - Получение токена
- `GET /api/auth/me` - Информация о текущем пользователе

### Пользователи
- `GET /api/users/` - Список пользователей
- `POST /api/users/` - Создание пользователя
- `GET /api/users/{user_id}` - Информация о пользователе

### Поездки
- `GET /api/trips/` - Список поездок
- `POST /api/trips/` - Создание поездки
- `GET /api/trips/{trip_id}` - Информация о поездке
- `PATCH /api/trips/{trip_id}` - Обновление поездки
- `DELETE /api/trips/{trip_id}` - Удаление поездки

### Места
- `GET /api/places/search` - Поиск мест
- `POST /api/places/` - Создание места

### Предложения
- `GET /api/suggestions/trip/{trip_id}` - Предложения для поездки
- `POST /api/suggestions/trip/{trip_id}` - Создание предложения
- `POST /api/suggestions/{suggestion_id}/vote` - Голосование

### Расходы
- `GET /api/expenses/trip/{trip_id}` - Расходы поездки
- `POST /api/expenses/` - Создание расхода
- `GET /api/expenses/trip/{trip_id}/balances` - Балансы поездки

## Разработка

### Добавление новых роутов

1. Создайте новый файл в `backend/app/routers/`
2. Определите роуты с помощью FastAPI
3. Добавьте роутер в `backend/app/main.py`

### Миграции базы данных

1. Создайте новую миграцию:
   ```bash
   alembic revision --autogenerate -m "description"
   ```

2. Примените миграцию:
   ```bash
   alembic upgrade head
   ```

### Добавление тестов

- Backend тесты размещаются в `backend/tests/`
- Frontend тесты размещаются в `frontend/src/__tests__/`

## Конфигурация

### Переменные окружения

Backend:
- `DATABASE_URL` - URL подключения к базе данных
- `SECRET_KEY` - Секретный ключ для JWT
- `DEBUG` - Режим отладки
- `APP_NAME` - Название приложения

Frontend:
- `REACT_APP_API_URL` - URL API сервера

## Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для вашей фичи (`git checkout -b feature/AmazingFeature`)
3. Закоммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## Лицензия

Этот проект лицензирован под MIT License. Подробности в файле LICENSE.

## Поддержка

Если у вас есть вопросы или проблемы, пожалуйста:
1. Проверьте существующие Issues
2. Создайте новый Issue с подробным описанием
3. Укажите версию приложения и окружение

---

**Trip Planner** - сделайте планирование путешествий проще и веселее! 🌍✈️
