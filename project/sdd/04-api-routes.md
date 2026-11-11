# 4. API и маршруты

## 4.1 Обзор маршрутов

| Метод | URL | Функция | Описание |
|-------|-----|---------|----------|
| GET | `/` | `index()` | Главная страница |
| GET | `/task/<task_id>` | `task()` | Страница задачи |
| POST | `/solve/<task_id>` | `solve()` | Решение задачи |
| GET | `/login` | `login()` | Страница входа |
| POST | `/login` | `login()` | Обработка входа |
| GET | `/register` | `register()` | Страница регистрации |
| POST | `/register` | `register()` | Обработка регистрации |
| GET | `/logout` | `logout()` | Выход из аккаунта |
| GET | `/math` | `math()` | Страница математики |
| GET | `/math/task/<task_id>` | `math_task()` | Страница матем. задачи |
| POST | `/math/solve/<task_id>` | `math_solve()` | Решение матем. задачи |
| GET | `/history` | `history()` | История решений |
| POST | `/history/clear` | `history_clear()` | Очистка истории |
| GET | `/reference` | `reference()` | Справочник |
| GET | `/builder` | `builder()` | Конструктор задач |
| POST | `/builder/solve` | `builder_solve()` | Решение конструктора |
| GET | `/profile` | `profile()` | Профиль пользователя |

## 4.2 Детальное описание

### 4.2.1 Главная страница

**GET /**

**Параметры:** Нет

**Ответ:** `index.html`

**Данные:**
```python
{
    'user': User | None,
    'groups': dict,  # {category: [(task_id, task_data), ...]}
    'total': int,    # Общее количество задач
    'records': list  # История решений
}
```

### 4.2.2 Авторизация

**POST /login**

**Форм-данные:**
- `username` (str) — имя пользователя
- `password` (str) — пароль

**Успех:** Redirect на `/`

**Ошибка:** `login.html` с сообщением

**POST /register**

**Форм-данные:**
- `username` (str)
- `email` (str)
- `password` (str)
- `password_confirm` (str)

**Валидация:**
- Длина пароля ≥ 6 символов
- Пароли совпадают
- Username и email уникальны

### 4.2.3 Решение физических задач

**POST /solve/<task_id>**

**Форм-данные:** Зависят от задачи (quantities)

**Параметры:**
- `task_id` (str) — ID задачи

**Процесс:**
1. Проверка аутентификации
2. Загрузка задачи
3. Парсинг входных данных
4. Вызов решателя `task['solve'](known, target)`
5. Генерация графика (если есть)
6. Сохранение в историю
7. Начисление XP и монет

**Ответ:** `result.html` с результатами

### 4.2.4 Решение математических задач

**POST /math/solve/<task_id>**

**Форм-данные:** Зависят от задачи

**Параметры:**
- `task_id` (str) — ID задачи
- `unknown` (str) — что нужно найти (опционально)

**Процесс:**
1. Проверка аутентификации
2. Задача из `MATH_TASKS`
3. Вызов `task['solve'](request.form)`
4. Сохранение в историю
5. Начисление 15 XP и 10 монет

**Ответ:** `math_task.html` с результатами

### 4.2.5 Конструктор задач

**POST /builder/solve**

**Форм-данные:**
- `task_type` (str) — тип задачи
- `unknown` (str) — неизвестная величина
- `body_N_c` (float) — теплоёмкость тела N
- `body_N_mass` (float) — масса тела N
- `body_N_temp` (float) — температура тела N
- `body_N_material` (str) — материал тела N

**Процесс:**
1. Парсинг данных о телах
2. Минимум 2 тела
3. Расчёт теплового баланса
4. Генерация SVG-визуализации

**Ответ:** `result_builder.html`

## 4.3 Session-данные

| Ключ | Тип | Описание |
|------|-----|----------|
| `user_id` | int | ID пользователя |
| `username` | str | Имя пользователя |

## 4.4 Ошибки

| Код | Описание |
|-----|----------|
| 404 | Страница не найдена |
| 500 | Внутренняя ошибка (обрабатывается в try/except) |

**Формат ошибок:**
- Flash-сообщения для UI
- ValueError для решателей задач

## 4.5 Middleware

### Аутентификация

```python
user = get_current_user()
if not user:
    flash('Войдите в аккаунт', 'warning')
    return redirect(url_for('login'))
```

### Flash-сообщения

```python
flash('Добро пожаловать!', 'success')
flash('Ошибка ввода', 'error')
```
