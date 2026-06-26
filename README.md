RelayCore

RelayCore — backend-платформа для VPN-сервиса, предназначенная для управления распределённой сетью узлов (relay nodes),
мониторинга их состояния и дальнейшего масштабирования VPN-инфраструктуры.

Статус проекта

🚧 Проект находится в активной разработке
Функциональность и API могут существенно меняться.

⸻

Текущий функционал

На данный момент доступно:

* Просмотр списка VPN-узлов
* Получение информации о каждом узле
* Базовая структура для дальнейшего управления узлами

⸻

Планируемые возможности

* Аутентификация и управление пользователями
* Ролевая модель доступа
* Управление узлами (создание / удаление / настройка)
* Health-check системы узлов
* Очереди событий и асинхронная обработка (RabbitMQ)
* Метрики и мониторинг состояния сети
* Поддержка масштабируемой VPN-архитектуры

⸻

Технологический стек

* Python 3.13+
* FastAPI
* SQLAlchemy (async)
* PostgreSQL
* RabbitMQ
* Alembic
* Pydantic v2
* Docker / Docker Compose
* Pytest

⸻

Архитектура

Проект построен вокруг модульной backend-архитектуры:

* API слой (FastAPI)
* Сервисный слой (business logic)
* Репозитории (работа с БД)
* Асинхронные воркеры (RabbitMQ)

⸻

Запуск проекта (локально)

```bash
git clone https://github.com/your-username/RelayCore.git
cd RelayCore
python -m venv .venv
source .venv/bin/activate
uv sync
```

Настройка окружения

Создай .env:

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/relaycore
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
SECRET_KEY=your-secret-key

⸻

Запуск через Docker

docker compose up --build

⸻

API документация

После запуска:

* Swagger: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

⸻

Тестирование

pytest

⸻

Примечания

Проект развивается как основа для будущей VPN-инфраструктуры с распределённой сетью узлов и управлением через backend
API.

⸻
