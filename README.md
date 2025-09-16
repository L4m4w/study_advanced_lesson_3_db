# Микросервис на **Python + FastAPI**, Автотесты для него и [reqres.in](https://reqres.in/) API.

## Эндпоинты Микросервиса

| Метод  | URL | Описание                      |
|--------|-----|-------------------------------|
| `GET`  | `/api/users/{user_id}` | Получить пользователя         |
| `GET`  | `/api/users` | Получить список пользователей |

## Запуск


1. **Склонировать репозиторий**
2. **Создать и активировать виртуальное окружение**
```bash
    python -m venv .venv
    source .venv/bin/activate # Linux/macOS  
    .\.venv\Scripts\activate   # Windows  
```
3. **Установить зависимости:**
```bash
  poetry install
```

4. **Запустить сервис:**
```bash
    cd qa_study_lesson_1/api_service/
    uvicorn api_service:app --reload
```
5. **Запустить тесты:**
- Для первого задания
```bash
    pytest -v -m regresin
```
- Для второго задания
```bash
    pytest -v -m local
```

## Модули

- `api_service` - основной сервис
- `tests` - автотесты
