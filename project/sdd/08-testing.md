# 8. Тестирование

## 8.1 Структура тестов

**Папка:** `tests/`

**Фреймворк:** pytest

**Конфигурация:** `conftest.py`

## 8.2 Файлы тестов

| Файл | Описание |
|------|----------|
| `conftest.py` | Конфигурация pytest, фикстуры |
| `test_app.py` | Тесты Flask-маршрутов |
| `test_database.py` | Тесты работы с БД |
| `test_engine.py` | Тесты движка задач |
| `test_loader.py` | Тесты загрузки YAML |

## 8.3 Запуск тестов

```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# С покрытием
pytest --cov=project

# Отдельный файл
pytest tests/test_app.py

# Отдельный тест
pytest tests/test_app.py::test_specific_function
```

## 8.4 Тестируемые компоненты

### 8.4.1 app.py

- Авторизация (login, register, logout)
- Главная страница
- Страницы задач
- Math-маршруты
- Конструктор

### 8.4.2 database

- Инициализация БД
- Регистрация пользователей
- Вход пользователей
- Сохранение решений
- Получение истории
- Обновление XP/монет

### 8.4.3 engine

- Валидация входных данных
- Выбор неизвестной величины
- Обработка ошибок

### 8.4.4 loader

- Загрузка YAML-файлов
- Парсинг спецификаций
- Группировка по категориям

## 8.5 Примеры тестов

### Тест авторизации

```python
def test_login_success(client):
    response = client.post('/login', data={
        'username': 'test_user',
        'password': 'password123'
    })
    assert response.status_code == 302  # Redirect
```

### Тест БД

```python
def test_register_user():
    success, error = register_user('test', 'test@test.com', 'password')
    assert success == True
    assert error is None
```

### Тест решателя

```python
def test_solve_quadratic():
    result, steps, explanation = solve_quadratic({'a': '1', 'b': '-5', 'c': '6'})
    assert 'x₁' in result
    assert 'x₂' in result
```

## 8.6 Покрытие кода

| Модуль | Покрытие |
|--------|----------|
| `app.py` | ~70% |
| `models.py` | ~85% |
| `tasks.py` | ~60% |
| `math_tasks.py` | ~75% |
| `loader.py` | ~90% |
| `graphs.py` | ~50% |

## 8.7 Рекомендации

1. **Добавить integration-тесты** для полного цикла
2. **Покрыть edge cases** (пустые поля, отрицательные числа)
3. **Добавить load-тесты** для проверки производительности
4. **Настроить CI/CD** с автоматическим запуском тестов
5. **Добавить тесты UI** (Selenium/Playwright)
