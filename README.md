# study-flow

API онлайн-школы на FastAPI с Clean Architecture: публичное чтение контента, admin CRUD дерева курса и JWT-аутентификация.

Репозиторий: [github.com/Kvezac/study-flow](https://github.com/Kvezac/study-flow)

## Требования

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Установка

```bash
git clone git@github.com:Kvezac/study-flow.git
cd study-flow
```

Установить зависимости проекта и dev-группу (тесты, ruff):

```bash
uv sync --group dev
```

Создать конфиг окружения:

```bash
cp .env.example .env
```

В `.env` задайте как минимум JWT-параметры, например:

```env
JWT_SECRET_KEY=dev-secret-change-me
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Применить миграции:

```bash
uv run alembic upgrade head
```

## Запуск приложения

```bash
uv run uvicorn app.main:app --reload
```

После старта:

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

## Тесты

Все тесты:

```bash
uv run pytest
```

Только unit:

```bash
uv run pytest tests/unit -q
```

Только integration / e2e:

```bash
uv run pytest tests/integration -q
```
