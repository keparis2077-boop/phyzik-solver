# Архитектура проекта ФИЗИК — Решебник

## 📋 Содержание

1. [Общая архитектура](#1-общая-архитектура)
2. [Структура файлов](#2-структура-файлов)
3. [Подробное описание модулей](#3-подробное-описание-модулей)
4. [Маршруты (Routes)](#4-маршруты-routes)
5. [База данных](#5-база-данных)
6. [Система задач](#6-система-задач)
7. [Геймификация](#7-геймификация)
8. [Аутентификация](#8-аутентификация)
9. [Как добавить новую задачу](#9-как-добавить-новую-задачу)
10. [Как добавить новый раздел](#10-как-добавить-новый-раздел)

---

## 1. Общая архитектура

Проект построен на **Flask** (Python) и состоит из:
- **Backend** — Flask-приложение с маршрутами и бизнес-логикой
- **Frontend** — HTML-шаблоны Jinja2 + CSS + JavaScript
- **База данных** — SQLite (через SQLAlchemy)
- **Задачи** — YAML-спецификации + Python-функции решения
- **Геймификация** — XP, монеты, серии, прогресс

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│  HTML (Jinja2) + CSS + JavaScript + MathJax (формулы)       │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP requests (POST/GET)
┌──────────────────────▼──────────────────────────────────────┐
│                     Backend (Flask)                          │
│  app.py — маршруты + контроллеры                            │
│  models.py — ORM модели (User, Solution)                    │
│  database.py — SQLAlchemy инициализация                      │
│  loader.py — загрузка YAML-спецификаций                      │
│  engine.py — движок решения задач по спецификации            │
│  math_tasks.py — задачи математики (Python-функции)          │
│  equation_solver.py — символьный решатель (sympy)            │
│  inequality_solver.py — решатель неравенств                  │
│  graphs.py — генерация SVG-графиков                          │
│  reference.py — константы и формулы                          │
│  history.db — база истории решений                           │
└──────────────────────┬──────────────────────────────────────┘
                       │ SQLAlchemy ORM
┌──────────────────────▼──────────────────────────────────────┐
│                    SQLite Database                           │
│  users | solutions | history                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Структура файлов

```
project/
├── app.py                    # ← Главный файл: маршруты + контроллеры
├── models.py                 # ← SQLAlchemy модели (User, Solution)
├── database.py               # ← Инициализация БД (init_db)
├── loader.py                 # ← Загрузка YAML-спецификаций → TASKS
├── engine.py                 # ← Движок решения: solve_task()
├── math_tasks.py             # ← Математические задачи + solve_*()
├── equation_solver.py        # ← Решатель уравнений (sympy)
├── inequality_solver.py      # ← Решатель неравенств (sympy)
├── graphs.py                 # ← Генерация SVG-графиков
├── reference.py              # ← Константы и формулы
├── requirements.txt          # ← Зависимости: flask, pyyaml, sympy
├── specs/                    # ← YAML-спецификации задач по физике
│   ├── kinematics.yaml       #   Кинематика
│   ├── dynamics.yaml         #   Динамика
│   ├── electricity.yaml      #   Электричество
│   ├── chemistry.yaml        #   Химия
│   └── ...                   #   Остальные разделы
├── templates/                # ← HTML-шаблоны
│   ├── base.html             #   ← Базовый шаблон (шапка, навигация, подвал)
│   ├── index.html            #   Главная страница (физика)
│   ├── math.html             #   Страница математики
│   ├── chemistry.html        #   Страница химии
│   ├── task.html             #   Страница задачи (форма ввода)
│   ├── result.html           #   Страница результата
│   ├── math_task.html        #   Страница математической задачи
│   ├── equation.html         #   Решатель уравнений
│   ├── search.html           #   Поиск по задачам
│   ├── reference.html        #   Справочник формул
│   ├── builder.html          #   Конструктор задач
│   ├── history.html          #   История решений
│   └── ...
├── static/
│   ├── style.css             # ← Основные стили
│   ├── script.js             # ← JavaScript (тема, анимации)
│   └── img/                  # ← Изображения
└── history.db                # ← SQLite база истории решений
```

---

## 3. Подробное описание модулей

### `app.py` — Главный файл (контроллеры)

**Задача:** Определяет все URL-маршруты и обрабатывает HTTP-запросы.

**Основные компоненты:**

```python
# Импорт модулей
from flask import Flask, render_template, request, ...
from loader import TASKS                              # Задачи физики (из YAML)
from math_tasks import MATH_TASKS                     # Задачи математики
from equation_solver import solve_equation            # Решатель уравнений
from models import init_db, register_user, login_user # БД + авторизация

# Создание приложения
app = Flask(__name__)
app.secret_key = '...'

# Маршруты (примеры)
@app.route('/')                           # Главная страница
@app.route('/task/<task_id>')             # Страница задачи
@app.route('/solve/<task_id>', methods=['POST'])  # Решение задачи
@app.route('/math')                       # Математика
@app.route('/equation')                   # Решатель уравнений
@app.route('/search')                     # Поиск
```

**Как работает маршрут `/solve`:**

```
1. Получить task_id из URL
2. Найти задачу в TASKS[task_id]
3. Извлечь известные значения из формы (request.form)
4. Вызвать t['solve'](known, target) — функция решения
5. Сохранить решение в БД (save_solution)
6. Начислить XP и монеты (add_xp, add_coins)
7. Сгенерировать график (если есть graph_type)
8. Вернуть шаблон result.html с результатами
```

---

### `loader.py` — Загрузчик задач

**Задача:** Читает YAML-файлы из `specs/` и формирует словарь `TASKS`.

**Как работает:**

```python
# 1. Загружает все YAML-файлы из specs/
templates = load_specs(Path('specs'))

# 2. Для каждой спецификации создаёт задачу
for task_id, tmpl in templates.items():
    TASKS[task_id] = {
        'name': tmpl['name'],
        'category': tmpl['category'],
        'icon': tmpl['icon'],
        'quantities': {...},      # {ключ: (название, единица)}
        'targets': {...},          # {ключ: название для выпадающего списка}
        'solve': lambda known, target: solve_task(tmpl, known, target),
        'graph_type': tmpl.get('graph_type'),
    }
```

**Результат:** `TASKS` — словарь вида:
```python
{
    'kinematics': {
        'name': 'Кинематика',
        'category': 'Кинематика',
        'quantities': {
            'v0': ('Начальная скорость v₀', 'м/с'),
            'v': ('Конечная скорость v', 'м/с'),
            't': ('Время t', 'с'),
            'S': ('Путь S', 'м'),
        },
        'targets': {
            'S': 'Путь S',
            'a': 'Ускорение a',
        },
        'solve': <функция>,
    },
    ...
}
```

---

### `engine.py` — Движок решения

**Задача:** Выполняет расчёты по YAML-спецификации.

**Как работает `solve_task(template, inputs, target)`:**

```python
def solve_task(template, inputs, target):
    # 1. Находит решение по target
    for sol in template['solutions']:
        if sol['target'] == target:
            # Проверяет, что все required переменные есть во вводе
            if set(sol['requires']).issubset(set(inputs.keys())):
                solution = sol
                break
    
    # 2. Вычисляет результат по формуле
    result_value = eval(solution['formula'], inputs)
    # Пример: formula = "m / n", inputs = {'m': 36, 'n': 2}
    # result_value = 18.0
    
    # 3. Проверяет constraints (ограничения)
    validate_constraints(solution['constraints'], inputs)
    
    # 4. Формирует шаги решения
    steps = []
    for step_template in solution['steps']:
        step = step_template.format(
            m=inputs.get('m'),
            n=inputs.get('n'),
            result=result_value,
        )
        steps.append(step)
    
    return results, steps, explanation
```

**Пример YAML-спецификации:**

```yaml
id: molar_mass
name: "Молярная масса"
variables:
  m:  { label: "Масса m", unit: "г", type: float }
  n:  { label: "n", unit: "моль", type: float }
  M:  { label: "M", unit: "г/моль", type: float }
solutions:
  - id: M_from_mn
    target: M
    requires: [m, n]
    formula: "m / n"
    steps:
      - "Формула: M = m/n"
      - "M = {m} / {n} = {result:.2f} г/моль"
```

---

### `math_tasks.py` — Математические задачи

**Задача:** Содержит задачи математики с Python-функциями решения.

**Структура:**

```python
MATH_TASKS = {
    'quadratic_equation': {
        'id': 'quadratic_equation',
        'name': 'Квадратное уравнение',
        'category': 'Алгебра',
        'difficulty': '8-9',
        'condition': 'Решите квадратное уравнение ax² + bx + c = 0',
        'formulas': ['D = b² - 4ac', 'x = (-b ± √D) / 2a'],
        'inputs': {
            'a': {'label': 'a', 'placeholder': 'Например: 1'},
            'b': {'label': 'b', 'placeholder': 'Например: -5'},
            'c': {'label': 'c', 'placeholder': 'Например: 6'},
        },
        'solve': lambda data: solve_quadratic(data),
    },
    ...
}

def solve_quadratic(data):
    a = float(data.get('a', 0))
    b = float(data.get('b', 0))
    c = float(data.get('c', 0))
    
    D = b**2 - 4*a*c
    steps = [
        f"D = b² - 4ac = {b}² - 4·{a}·{c} = {D}",
        ...
    ]
    
    if D < 0:
        return {}, steps, "Корней нет"
    elif D == 0:
        x = -b / (2*a)
        return {'x': str(x)}, steps, "Один корень"
    else:
        x1 = (-b + D**0.5) / (2*a)
        x2 = (-b - D**0.5) / (2*a)
        return {'x₁': str(x1), 'x₂': str(x2)}, steps, "Два корня"
```

**Доступные задачи:**
- Алгебра: квадратное, линейное уравнение, система, неравенства
- Геометрия: площадь треугольника/круга, теорема Пифагора
- Тригонометрия: sin/cos/tan, теорема косинусов
- Анализ: производная, интеграл, предел
- Векторы: сложение, скалярное произведение, проекция
- Теория вероятностей: классическая, комбинаторика, Бернулли

---

### `equation_solver.py` — Решатель уравнений

**Задача:** Символьное решение уравнений с помощью `sympy`.

**Функции:**

```python
solve_equation("2*x + 5 = 15", variable="x")
# → {
#     'solutions': ['x = 5'],
#     'steps': [...],
#     'type': 'линейное',
#     'full_equation': '2x - 10 = 0',
# }

simplify_expression_only("4/8")
# → {
#     'simplified': '1/2',
#     'numerator': 1,
#     'denominator': 2,
#     'decimal': '0.5',
#     'is_fraction': True,
# }

solve_system_of_equations(["2*x + y = 10", "x - y = 2"])
# → {
#     'solutions': ['x = 4', 'y = 2'],
# }
```

**Как работает:**

1. **Парсинг** — преобразует строку `2*x + 5 = 15` в sympy-выражение
2. **Упрощение** — переносит всё в левую часть: `2*x - 10 = 0`
3. **Определение типа** — считает степень полинома
4. **Решение** — вызывает `sympy.solve()`
5. **Форматирование** — показывает красивые шаги решения

---

### `inequality_solver.py` — Решатель неравенств

**Задача:** Решение линейных и квадратичных неравенств.

**Функции:**

```python
solve_inequality("2*x - 6 > 0")
# → {
#     'solution': 'x ∈ (3, +∞)',
#     'steps': [...],
# }

solve_inequality("x^2 - 5*x + 6 > 0")
# → {
#     'solution': 'x ∈ (-∞, 2) ∪ (3, +∞)',
# }
```

**Метод:**
1. Находит корни уравнения
2. Строит числовую прямую с точками
3. Определяет знак на каждом интервале
4. Возвращает объединение интервалов

---

### `graphs.py` — Генерация графиков

**Задача:** Создаёт SVG-графики для физических задач.

```python
generate_graph('kinematics', {'v0': 10, 'a': 2, 't': 5})
# → SVG-строка с графиком зависимости пути от времени
```

**Поддерживаемые типы:**
- `kinematics` — путь от времени
- `freefall` — высота при свободном падении
- `ballistics` — траектория
- `ohm` — вольт-амперная характеристика
- `energy` — энергия от времени
- `pressure` — давление

---

### `models.py` — Модели БД

**Задача:** SQLAlchemy модели для хранения пользователей и решений.

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    xp = db.Column(db.Integer, default=0)
    coins = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    
class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.String(100))
    task_name = db.Column(db.String(200))
    inputs = db.Column(db.Text)
    results = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
```

---

### `reference.py` — Справочник

**Задача:** Хранит константы и формулы.

```python
CONSTANTS = {
    'g': {'name': 'Ускорение свободного падения', 'value': '9.81', 'unit': 'м/с²'},
    'c': {'name': 'Скорость света', 'value': '3×10⁸', 'unit': 'м/с'},
    ...
}

FORMULAS = {
    'kinematics': [
        {'name': 'Скорость', 'formula': 'v = v₀ + at'},
        {'name': 'Путь', 'formula': 'S = v₀t + at²/2'},
        ...
    ],
    ...
}
```

---

## 4. Маршруты (Routes)

| URL | Метод | Функция | Описание |
|-----|-------|---------|----------|
| `/` | GET | `index()` | Главная страница (физика) |
| `/task/<task_id>` | GET | `task()` | Страница задачи |
| `/solve/<task_id>` | POST | `solve()` | Решение физической задачи |
| `/math` | GET | `math()` | Страница математики |
| `/math/task/<task_id>` | GET | `math_task()` | Страница математической задачи |
| `/math/solve/<task_id>` | POST | `math_solve()` | Решение математической задачи |
| `/chemistry` | GET | `chemistry()` | Страница химии |
| `/chemistry/task/<task_id>` | GET | `chemistry_task()` | Страница химической задачи |
| `/chemistry/solve/<task_id>` | POST | `chemistry_solve()` | Решение химической задачи |
| `/equation` | GET | `equation()` | Решатель уравнений |
| `/equation/solve` | POST | `equation_solve()` | Решение уравнения |
| `/reference` | GET | `reference()` | Справочник формул |
| `/builder` | GET | `builder()` | Конструктор задач |
| `/builder/solve` | POST | `builder_solve()` | Решение задачи конструктора |
| `/search` | GET | `search()` | Поиск по задачам |
| `/history` | GET | `history()` | История решений |
| `/login` | GET/POST | `login()` | Авторизация |
| `/register` | GET/POST | `register()` | Регистрация |
| `/logout` | GET | `logout()` | Выход |
| `/profile` | GET | `profile()` | Профиль пользователя |

---

## 5. База данных

**Технология:** SQLite через SQLAlchemy

**Таблицы:**

```
users:
  id, username, email, password_hash, xp, coins, streak, created_at

solutions:
  id, user_id, task_id, task_name, inputs, results, timestamp

history.db (отдельный файл):
  Аналогичная структура для истории решений
```

**Инициализация:**
```python
# database.py
from models import db
db.init_app(app)
db.create_all()  # Создаёт таблицы при запуске
```

---

## 6. Система задач

### Физика (YAML-спецификации)

**Формат файла `specs/kinematics.yaml`:**

```yaml
templates:
  - id: kinematics
    name: "Кинематика"
    category: "Кинематика"
    icon: "🏃"
    variables:
      v0: { label: "Начальная скорость v₀", unit: "м/с", type: float }
      v:  { label: "Конечная скорость v", unit: "м/с", type: float }
      t:  { label: "Время t", unit: "с", type: float }
      S:  { label: "Путь S", unit: "м", type: float }
      a:  { label: "Ускорение a", unit: "м/с²", type: float }
    solutions:
      - id: find_S
        target: S
        requires: [v0, t, a]
        formula: "v0 * t + 0.5 * a * t**2"
        steps:
          - "Формула: S = v₀t + at²/2"
          - "S = {v0}·{t} + 0.5·{a}·{t}² = {result:.2f} м"
      - id: find_a
        target: a
        requires: [v0, v, t]
        formula: "(v - v0) / t"
        steps:
          - "Формула: a = (v - v₀) / t"
          - "a = ({v} - {v0}) / {t} = {result:.2f} м/с²"
```

**Процесс загрузки:**
```
YAML → loader.py → TASKS[task_id] → solve_task() → результат
```

### Математика (Python-функции)

**Формат `math_tasks.py`:**

```python
MATH_TASKS = {
    'quadratic_equation': {
        'inputs': {...},
        'solve': lambda data: solve_quadratic(data),
    },
}

def solve_quadratic(data):
    # Возвращает: (results_dict, steps_list, explanation_str)
    ...
```

---

## 7. Геймификация

**Система вознаграждений:**

| Действие | XP | Монеты |
|----------|-----|--------|
| Решение физики | +10 | +5 |
| Решение химии | +10 | +5 |
| Решение математики | +15 | +10 |
| Решение уравнений | +20 | +15 |
| Конструктор | +15 | +10 |

**Серия (streak):**
- Считается количество дней подряд с решениями
- Обновляется при каждом решении

**Хранение:**
```python
# models.py
class User(db.Model):
    xp = db.Column(db.Integer, default=0)
    coins = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)

# app.py
def add_xp(user_id, amount):
    user = get_user_by_id(user_id)
    user.xp += amount
    db.session.commit()
```

---

## 8. Аутентификация

**Механизм:** Сессии Flask + хеширование паролей

**Процесс регистрации:**
```
1. Пользователь вводит: username, email, password
2. Пароль хешируется: generate_password_hash(password)
3. Создаётся запись в БД
4. Перенаправление на страницу входа
```

**Процесс входа:**
```
1. Пользователь вводит: username, password
2. Проверяется хеш: check_password_hash(user.password_hash, password)
3. Если совпало → session['user_id'] = user.id
4. Перенаправление на главную
```

**Проверка авторизации:**
```python
def get_current_user():
    if 'user_id' in session:
        return get_user_by_id(session['user_id'])
    return None
```

---

## 9. Как добавить новую задачу

### Для физики (YAML):

1. **Создать файл** `specs/my_topic.yaml`:
```yaml
templates:
  - id: my_task
    name: "Моя задача"
    category: "Моя тема"
    icon: "🎯"
    variables:
      x: { label: "X", unit: "ед", type: float }
      y: { label: "Y", unit: "ед", type: float }
    solutions:
      - id: find_y
        target: y
        requires: [x]
        formula: "x * 2"
        steps:
          - "Y = 2X"
          - "Y = {x} · 2 = {result:.2f}"
```

2. **Перезапустить сервер** — задача автоматически загрузится

### Для математики:

1. **Добавить задачу** в `MATH_TASKS` в `math_tasks.py`:
```python
'my_math_task': {
    'id': 'my_math_task',
    'name': 'Моя задача',
    'category': 'Алгебра',
    'difficulty': '8',
    'condition': 'Описание задачи',
    'formulas': ['формула 1', 'формула 2'],
    'inputs': {
        'a': {'label': 'a', 'placeholder': 'Введите a'},
    },
    'solve': lambda data: solve_my_task(data),
},
```

2. **Добавить функцию** решения:
```python
def solve_my_task(data):
    a = float(data.get('a', 0))
    result = a * 2
    steps = [f"a = {a}", f"Результат = {result}"]
    return {'result': str(result)}, steps, "Пояснение"
```

---

## 10. Как добавить новый раздел

1. **Добавить маршрут** в `app.py`:
```python
@app.route('/my_section')
def my_section():
    return render_template('my_section.html')
```

2. **Создать шаблон** `templates/my_section.html`

3. **Добавить ссылку** в `templates/base.html`:
```html
<a href="{{ url_for('my_section') }}">Мой раздел</a>
```

4. **Добавить в мобильную навигацию** внизу `base.html`

---

## Поток данных: пример решения задачи

```
Пользователь
    │
    │ 1. Открывает /task/kinematics
    ▼
templates/task.html
    │ 2. Показывает форму с полями v0, v, t, S, a
    │    и выпадающим списком "Что найти?"
    ▼
Пользователь вводит: v0=10, v=30, t=5, находит: a
    │
    │ 3. Отправляет POST /solve/kinematics
    ▼
app.py → solve()
    │ 4. known = {'v0': 10, 'v': 30, 't': 5}
    │ 5. target = 'a'
    │ 6. t['solve'](known, target) → solve_task(template, known, 'a')
    ▼
engine.py → solve_task()
    │ 7. Находит solution с target='a'
    │ 8. formula = "(v - v0) / t"
    │ 9. result = (30 - 10) / 5 = 4.0
    │ 10. Формирует шаги
    ▼
    │ 11. Возвращает:
    │    results = {'a': '4.00'}
    │    steps = ['a = (v - v₀) / t', 'a = (30 - 10) / 5 = 4.00']
    │    explanation = '...'
    ▼
app.py
    │ 12. save_solution(user_id, ...)
    │ 13. add_xp(user_id, 10)
    │ 14. generate_graph('kinematics', known)
    ▼
templates/result.html
    │ 15. Показывает:
    │    - Дано: v0=10, v=30, t=5
    │    - Найти: a
    │    - Ответ: a = 4.00 м/с²
    │    - Шаги решения
    │    - График
    ▼
Пользователь видит результат
```

---

## Итоговая схема

```
┌──────────────────────────────────────────────────────────────┐
│                        Пользователь                           │
│         (открывает задачу → вводит данные → видит результат)  │
└──────────────────────────┬───────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │   templates/*.html      │  ← Frontend
              │   (Jinja2 + CSS + JS)   │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │      app.py             │  ← Backend
              │   (маршруты + логика)   │
              └────┬──────────┬────────┘
                   │          │
      ┌────────────▼──┐  ┌───▼────────────┐
      │  loader.py    │  │  engine.py     │  ← Движок
      │  (YAML→TASKS) │  │  (формулы)     │
      └───────────────┘  └────────────────┘
                   │          │
      ┌────────────▼──────────▼────────────┐
      │     models.py / database.py        │  ← БД
      │     (SQLAlchemy + SQLite)          │
      └────────────────────────────────────┘
```
