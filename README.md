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

4. **Запустить сервис:**
- Запуск из api_service/api_service.py
5. **Запустить тесты:**
- Для первого задания
```bash
    pytest -v -m smoke
```
- Для четвертого и пятого заданий
```bash
    pytest -v -m pagination
```
##  Задание

1. Расположение: tests.test_smoke.TestSmokeApi

2. Расположение: api_service.api_service.status

3. Расположение: api_service.api_service.get_users

4. Расположение: tests.test_users.TestLocalApi.test_get_users_check_users_data_amount

5. Расположение: 
- tests.test_users.TestLocalApi.test_get_users_check_users_data_amount
- tests.test_users.TestLocalApi.test_get_users_data_check_by_size_param
- tests.test_users.TestLocalApi.test_get_users_data_check_by_page_param

## Модули

- `api_service` - основной сервис
- `tests` - автотесты
- `models` - базовые модели данных
