# Как вести разработку в Clean Architecture

## Главная идея

Фича — это **сценарий** (что система должна сделать), а не «эндпоинт» и не «таблица».

Слои:

| Слой           | Папка                 | Ответственность                 |
| :------------- | :-------------------- | :------------------------------ |
| Domain         | `app/domain/`         | Правила сущностей, инварианты   |
| Application    | `app/application/`    | Сценарии (use cases), контракты |
| Infrastructure | `app/infrastructure/` | БД, JWT, конкретные реализации  |
| Presentation   | `app/presentation/`   | HTTP, схемы, DI, handlers       |

Зависимости только внутрь: presentation → application → domain.  
Infrastructure реализует интерфейсы application.

---

## С чего начинать, если теряешься

Не с роута. Не с SQLAlchemy.

**Сначала опиши сценарий словами**, потом иди в `use_cases`.

Пример формулировки:

> «Нужно X. На входе — идентификатор/поля. Если сущности нет — ошибка. Нужно согласовать связанные сущности. В конце — один commit.»

Дальше работай **от use case наружу**.

---

## Рекомендуемый порядок реализации

### 1. Application: use case (скелет сценария)

Файл: `app/application/use_cases/<entity>/<action>_<entity>.py`
Пример: `app/application/use_cases/courses/delete_course.py`

В одном файле обычно:

1. `Command` / `Query` — входные данные (dataclass)
2. `XxxUseCase` — класс с `execute`

Шаблон:

```python
@dataclass(slots=True)
class DoSomethingCommand:
    entity_id: UUID
    # другие поля входа


class DoSomethingUseCase:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, command: DoSomethingCommand) -> ...:
        async with self.uow:
            # 1. загрузить нужные сущности
            # 2. проверить наличие → ApplicationError (*NotFoundError)
            # 3. применить доменные изменения (методы entity)
            # 4. сохранить через репозитории (add/update/remove)
            # 5. await self.uow.commit()
            # 6. вернуть результат (или None)
```

**Что писать в use case:**

- оркестрацию: кого загрузить, в каком порядке менять
- проверки «существует / не существует»
- вызовы domain-методов (`add_*`, `remove_*`, `update(...)`)
- вызовы репозиториев через `uow`
- `commit()` один раз в конце успешного пути

**Чего не писать в use case:**

- FastAPI / Request / Response
- SQLAlchemy / `session` / SQL
- детали JWT и HTTP-кодов

Если для сценария не хватает метода репозитория — **не лезь сразу в SQL**.  
Сначала зафиксируй нужный вызов в use case (`await self.uow.modules.remove(...)`), потом добавь его в контракт.

Use case на этом этапе может «не компилироваться» — это нормально: он задаёт контракт фичи.

---

### 2. Domain: правила сущности

Файл: `app/domain/entities/...`

Сюда выноси то, что про **состояние объекта**:

- валидация полей
- `update(...)`
- связь с детьми: `add_*` / `remove_*`

Сюда **не** клади:

- «удалить из БД»
- «сходить в соседний репозиторий»
- HTTP/SQL

Правило: domain меняет **память объекта**, persistence — задача application + repository.

---

### 3. Application: контракты репозиториев

Файл: `app/application/interfaces/repositories/...`

Спроси: «какие операции нужны сценарию?»

Типичный набор:

- `get_by_id` / `get_by_ids`
- `add`
- `update`
- `remove`

Добавляй в ABC только то, что реально вызывает use case.  
Не тащи инфраструктурные детали в сигнатуру (`Session`, `Model`, raw SQL).

Ошибки сценария — в `app/application/exceptions.py`  
(`*NotFoundError` и т.п.), не HTTPException.

---

### 4. Infrastructure: реализация контрактов

Файлы:

- `app/infrastructure/database/repositories/`
- при необходимости models / mappers / migrations

Здесь:

- SQLAlchemy `select` / `delete` / `flush`
- маппинг Model ↔ Domain entity
- ничего про HTTP и бизнес-оркестрацию дерева

Если UoW уже отдаёт этот репозиторий — новый use case обычно подключается без правок UoW.

---

### 5. Presentation: HTTP + DI

1. `dependencies.py` — фабрика use case  
   (`SqlAlchemyUnitOfWork(session_factory=SessionFactory)`)
2. `routes/...` — тонкий адаптер:
   - request → Command
   - `await use_case.execute(...)`
   - entity/DTO → response schema
3. auth/защита — на уровне router/dependencies, не внутри use case
4. коды ответов и 404/401/403 — через существующие handlers

Роут не должен знать про каскады и списки связей.  
Его задача: принять HTTP и вызвать сценарий.

---

### 6. Тесты: от сценария к системе

По слоям:

1. **Unit use case** + Fake UoW/репозитории  
   - happy path  
   - not found  
   - согласованность связанных сущностей в памяти
2. **E2E/API** (по необходимости)  
   - создать через API  
   - выполнить действие  
   - проверить публичное чтение  
   - проверить, что «лишнее» больше не читается

E2E показывает, что фича — изменение системы, а не точечный SQL.

---

## Карта «куда смотреть», когда пишешь use case

```text
Command (вход)
   ↓
UseCase.execute
   ↓
async with uow:
   репозиторий.get_*          → есть ли сущность?
   domain.method(...)         → бизнес-изменение в памяти
   репозиторий.add/update/remove
   uow.commit()
   ↓
return entity | None
```

Чеклист внутри `execute`:

1. Открыл UoW?
2. Загрузил всё, что нужно для согласованности?
3. Обработал `None` через application-исключения?
4. Изменил domain-состояние родителя/детей, если связи есть?
5. Сохранил все затронутые агрегаты?
6. Сделал один `commit`?
7. Не протащил FastAPI/SQLAlchemy в этот файл?

---

## Read vs Write в этом проекте

**Write** (create/update/delete):

- use case принимает `UnitOfWork`
- работает внутри `async with self.uow`
- сам коммитит

**Read** (get/list/structure):

- часто получает конкретные репозитории через DI
- без обязательного write-commit

Перед копированием соседа сначала посмотри: это read или write.

---

## Как не потеряться на практике

Когда берёшь новую фичу:

1. Напиши 3–5 пунктов сценария на бумаге/в комментарии.
2. Создай файл use case и Command.
3. Заполни `execute` «идеальным» кодом через `uow.*`.
4. Выпиши недостающее:
   - domain-метод
   - метод репозитория
   - exception
5. Реализуй недостающее по списку.
6. Подключи route + DI.
7. Покрой unit-тестом по образцу соседнего write-сценария.

Если застрял — вернись к вопросу:

> «Какой сценарий я оркестрирую в `execute`?»

Не к вопросу «какую таблицу обновить».

---

## Антипаттерны

- Сразу писать SQL в роуте или use case
- Дублировать бизнес-правила в handler и entity
- Забыть обновить/согласовать связанную сущность
- Несколько `commit` посреди сценария
- Подгонять domain под колонки БД вместо сценария
- Считать «удалил строку» = «фича готова» без проверки чтения снаружи

---

## Короткий девиз

**Сначала сценарий в `use_cases`, потом контракты, потом БД, потом HTTP.**

Use case — центр фичи. Остальные слои его обслуживают.
