# Микросервис на **Python + FastAPI**, Автотесты для него и [reqres.in](https://reqres.in/) API.

## Эндпоинты Микросервиса

| Метод | URL | Описание                                |
|-------|-----|-----------------------------------------|
| `GET` | `/api/users/{user_id}` | Получить пользователя                   |
| `GET` | `/api/users` | Получить список пользователей           |
| `GET` | `/status` | Получить cтaтус загрузки пользователей  |
| `GET` | `/api/status` | Получить cтaтус доступности раздела api |

## Запуск

1. **Склонировать репозиторий**
2. **Создать и активировать виртуальное окружение**
```bash
    python3 -m venv .venv
```
- Linux/macOS  
```bash
    source .venv/bin/activate 
```
- Windows
```bash
    source .\.venv\Scripts\activate     
```
3. **Установить зависимости:**
```bash
    poetry install
```

4. Создание .env файла
```bash
    cp .env.example .env
```

5. **Запустите Docker-контейнеры:**
```bash
    docker compose up -d
```

После этого API будет доступен по адресу **`http://127.0.0.1:8002`**.
##  Задание

1. Запустить postgresql в докере.
Запустить проект локально (в докере будем запускать в следующем занятии).
```bash
    docker compose up -d
```
2. Расширить тестовое покрытие:

- Тест на post: создание. Предусловия: подготовленные тестовые данные
- Тест на delete: удаление. Предусловия: созданный пользователь
- Тест на patch: изменение. Предусловия: созданный пользователь
```bash
    pytest -v -m http
```
Расположение тестов: 
- tests.test_users.TestLocalApi.test_create_user
- tests.test_users.TestLocalApi.test_delete_user
- tests.test_users.TestLocalApi.test_update_user

## Модули

- `api_service` - основной сервис
- `tests` - автотесты