# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from loader import TASKS, group_by_category, get_math_tasks_by_category
from reference import CONSTANTS, FORMULAS
from models import (
    init_db, register_user, login_user, get_user_by_id,
    save_solution, get_history, clear_history, add_xp, add_coins
)
from graphs import generate_graph
from math_tasks import MATH_TASKS

app = Flask(__name__)
app.secret_key = 'physics-solver-secret-key-2025'

# Инициализация базы данных
init_db()


CATEGORY_COLORS = {
    "Кинематика": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "Динамика": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
    "Электричество": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
    "Энергия": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
    "Давление": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
    "Термодинамика": "linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)",
    "Оптика": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",
}


def get_current_user():
    """Получает текущего пользователя из сессии."""
    if 'user_id' in session:
        return get_user_by_id(session['user_id'])
    return None


# ==================== АВТОРИЗАЦИЯ ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user = login_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Добро пожаловать, {user["username"]}!', 'success')
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Неверное имя пользователя или пароль')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        if password != password_confirm:
            return render_template('register.html', error='Пароли не совпадают')
        
        if len(password) < 6:
            return render_template('register.html', error='Пароль должен быть минимум 6 символов')
        
        success, error = register_user(username, email, password)
        if success:
            flash('Регистрация успешна! Войдите в аккаунт.', 'success')
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error=error)
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('index'))


# ==================== ОСНОВНЫЕ СТРАНИЦЫ ====================

@app.route('/')
def index():
    user = get_current_user()
    records = get_history(user['id']) if user else []
    
    # Исключаем математические категории из раздела Физика
    math_categories = {'Алгебра', 'Геометрия', 'Тригонометрия', 'Анализ', 'Векторы', 'Теория вероятностей'}
    groups = group_by_category()
    physics_groups = {k: v for k, v in groups.items() if k not in math_categories}
    
    return render_template('index.html',
                           user=user,
                           groups=physics_groups,
                           total=len(TASKS),
                           records=records)


@app.route('/task/<task_id>')
def task(task_id):
    if task_id not in TASKS:
        return redirect(url_for('index'))
    return render_template('task.html', task_id=task_id, task=TASKS[task_id])


@app.route('/solve/<task_id>', methods=['POST'])
def solve(task_id):
    user = get_current_user()
    if not user:
        flash('Войдите в аккаунт для сохранения результатов', 'warning')
        return redirect(url_for('login'))
    
    t = TASKS[task_id]

    if 'quantities' in t:
        target = request.form.get('target')
        if not target:
            return redirect(url_for('task', task_id=task_id))

        known = {}
        for key, (label, unit) in t['quantities'].items():
            if key == target:
                continue
            raw = request.form.get(key, '').strip()
            if raw:
                try:
                    known[key] = float(raw)
                except ValueError:
                    return render_template(
                        'result.html', task_id=task_id, task=t,
                        error=f"Некорректное число в поле «{label}»",
                        form=request.form, results={}, steps=[], explanation='',
                    )

        try:
            results, steps, explanation = t['solve'](known, target)
            error = None
            inputs_str = ', '.join(f"{k}={v}" for k, v in known.items()) + f' | найти: {target}'
            results_str = ', '.join(f"{k}={v}" for k, v in results.items())
            save_solution(user['id'], task_id, t['name'], inputs_str, results_str)
            add_xp(user['id'], 10)
            add_coins(user['id'], 5)
            
            graph_type = t.get('graph_type')
            graph_svg = None
            if graph_type:
                try:
                    graph_svg = generate_graph(graph_type, known)
                except Exception:
                    graph_svg = None
        except Exception as e:
            results, steps, explanation, graph_svg = {}, [], '', None
            error = str(e)

        return render_template(
            'result.html',
            task_id=task_id, task=t,
            results=results, steps=steps, explanation=explanation,
            error=error, form=request.form, graph_svg=graph_svg,
        )

    selected = request.form.getlist('outputs') or list(t.get('outputs', {}).keys())
    graph_svg = None
    try:
        results, steps, explanation = t['solve'](request.form, selected)
        error = None
        inputs_str = ', '.join(
            f"{label.split('(')[0].strip()}={request.form[key]} {unit}"
            for key, label, unit in t['inputs']
        )
        results_str = '; '.join(f"{k}: {v}" for k, v in results.items())
        save_solution(user['id'], task_id, t['name'], inputs_str, results_str)
        add_xp(user['id'], 10)
        
        graph_type = t.get('graph_type')
        if graph_type:
            try:
                graph_svg = generate_graph(graph_type, dict(request.form))
            except Exception:
                graph_svg = None
    except Exception as e:
        results, steps, explanation, graph_svg = {}, [], '', None
        error = f"Ошибка ввода: {e}"

    return render_template(
        'result.html',
        task_id=task_id, task=t,
        results=results, steps=steps, explanation=explanation,
        error=error, form=request.form, graph_svg=graph_svg,
    )


@app.route('/history')
def history():
    user = get_current_user()
    if not user:
        flash('Войдите в аккаунт', 'warning')
        return redirect(url_for('login'))
    
    records = get_history(user['id'])
    return render_template('history.html', records=records)


@app.route('/history/clear', methods=['POST'])
def history_clear():
    user = get_current_user()
    if user:
        clear_history(user['id'])
        flash('История очищена', 'success')
    return redirect(url_for('history'))


@app.route('/reference')
def reference():
    user = get_current_user()
    return render_template('reference.html', user=user, constants=CONSTANTS, formulas=FORMULAS)


# ==================== МАТЕМАТИКА ====================

@app.route('/math')
def math():
    user = get_current_user()
    if not user:
        flash('Войдите в аккаунт для сохранения результатов', 'warning')
        return redirect(url_for('login'))
    
    algebra_tasks = [t for t in MATH_TASKS.values() if t['category'] == 'Алгебра']
    geometry_tasks = [t for t in MATH_TASKS.values() if t['category'] == 'Геометрия']
    trigonometry_tasks = [t for t in MATH_TASKS.values() if t['category'] == 'Тригонометрия']
    analysis_tasks = [t for t in MATH_TASKS.values() if t['category'] == 'Анализ']
    vectors_tasks = [t for t in MATH_TASKS.values() if t['category'] == 'Векторы']
    probability_tasks = [t for t in MATH_TASKS.values() if t['category'] == 'Теория вероятностей']
    
    return render_template('math.html',
                           user=user,
                           algebra_tasks=algebra_tasks,
                           geometry_tasks=geometry_tasks,
                           trigonometry_tasks=trigonometry_tasks,
                           analysis_tasks=analysis_tasks,
                           vectors_tasks=vectors_tasks,
                           probability_tasks=probability_tasks)


@app.route('/math/task/<task_id>')
def math_task(task_id):
    if task_id not in MATH_TASKS:
        return redirect(url_for('math'))
    
    task = MATH_TASKS[task_id]
    return render_template('math_task.html', task=task, task_id=task_id, results=None, steps=[], explanation='', error=None)


@app.route('/math/solve/<task_id>', methods=['POST'])
def math_solve(task_id):
    user = get_current_user()
    if not user:
        flash('Войдите в аккаунт', 'warning')
        return redirect(url_for('login'))
    
    if task_id not in MATH_TASKS:
        return redirect(url_for('math'))
    
    task = MATH_TASKS[task_id]
    
    try:
        results, steps, explanation = task['solve'](request.form)
        error = None
        
        inputs_str = ', '.join(f"{k}={request.form[k]}" for k in task['inputs'].keys())
        results_str = ', '.join(f"{k}={v}" for k, v in results.items())
        save_solution(user['id'], task_id, task['name'], inputs_str, results_str)
        add_xp(user['id'], 15)
        add_coins(user['id'], 10)
        
    except Exception as e:
        results, steps, explanation = {}, [], ''
        error = str(e)
    
    return render_template('math_task.html',
                           task=task, task_id=task_id,
                           results=results, steps=steps, explanation=explanation,
                           error=error)


# ==================== КОНСТРУКТОР ====================

@app.route('/builder')
def builder():
    user = get_current_user()
    if not user:
        flash('Войдите в аккаунт для сохранения результатов', 'warning')
        return redirect(url_for('login'))
    return render_template('builder.html')


@app.route('/builder/solve', methods=['POST'])
def builder_solve():
    user = get_current_user()
    if not user:
        flash('Войдите в аккаунт', 'warning')
        return redirect(url_for('login'))
    
    category = request.form.get('category', 'physics')
    task_type = request.form.get('task_type', 'thermal_balance')
    unknown = request.form.get('unknown', 't_eq')
    
    import math
    
    steps = []
    explanation = ""
    answer_label = ""
    answer_value = ""
    task_type_name = ""
    unknown_label = ""
    bodies_info = []
    
    try:
        # ==================== ФИЗИКА ====================
        if category == 'physics':
            if task_type == 'thermal_balance':
                # Тепловые задачи с телами
                bodies = []
                body_num = 1
                while True:
                    c = request.form.get(f'body_{body_num}_c')
                    if not c:
                        break
                    try:
                        mass_str = request.form.get(f'body_{body_num}_mass')
                        temp_str = request.form.get(f'body_{body_num}_temp')
                        body = {
                            'c': float(c),
                            'mass': float(mass_str) if mass_str else None,
                            'temp': float(temp_str) if temp_str else None,
                            'material': request.form.get(f'body_{body_num}_material', 'water'),
                            'num': body_num
                        }
                        bodies.append(body)
                        body_num += 1
                    except (ValueError, TypeError):
                        body_num += 1
                
                if len(bodies) < 2:
                    return render_template(
                        'result_builder.html',
                        error="Нужно минимум 2 тела для задачи",
                        task_type_name="", bodies_info=[],
                        steps=[], explanation="",
                        answer_label="", answer_value="", graph_svg=None
                    )
                
                material_names = {
                    'water': 'Вода', 'ice': 'Лёд', 'aluminum': 'Алюминий',
                    'iron': 'Железо', 'copper': 'Медь', 'lead': 'Свинец',
                    'custom': 'Пользовательский'
                }
                
                task_type_name = 'Тепловое равновесие'
                
                if unknown == 't_eq':
                    numerator = sum(b['c'] * b['mass'] * b['temp'] for b in bodies)
                    denominator = sum(b['c'] * b['mass'] for b in bodies)
                    if denominator == 0:
                        raise ValueError("Сумма теплоёмкостей равна нулю")
                    t_eq = numerator / denominator
                    steps.append("Уравнение теплового баланса: Q_отданное = Q_полученное")
                    steps.append("Σ(c_i · m_i · t_i) / Σ(c_i · m_i) = t_равн")
                    steps.append(f"t_равн = {t_eq:.2f} °C")
                    answer_label = "Конечная температура"
                    answer_value = f"{t_eq:.2f} °C"
                    explanation = "При контакте тел тепло переходит от горячих к холодным."
                    
                elif unknown == 'mass':
                    target_body = bodies[-1]
                    other_bodies = bodies[:-1]
                    
                    # Используем заданную t_eq или вычисляем
                    t_eq_raw = request.form.get('t_eq', '').strip()
                    if t_eq_raw:
                        t_eq = float(t_eq_raw)
                        steps.append(f"Дано: t_равн = {t_eq:.2f} °C (задано)")
                    else:
                        t_eq = sum(b['c'] * b['mass'] * b['temp'] for b in other_bodies) / sum(b['c'] * b['mass'] for b in other_bodies)
                        steps.append(f"Находим t_равн: Σ(cᵢ·mᵢ·tᵢ) / Σ(cᵢ·mᵢ) = {t_eq:.2f} °C")
                    
                    numerator = sum(b['c'] * b['mass'] * (t_eq - b['temp']) for b in other_bodies)
                    denominator = target_body['c'] * (target_body['temp'] - t_eq)
                    if denominator == 0:
                        raise ValueError("Деление на ноль")
                    m_target = numerator / denominator
                    steps.append("Уравнение теплового баланса: Q_отданное = Q_полученное")
                    steps.append(f"m_{target_body['num']} = {m_target:.3f} кг")
                    answer_label = f"Масса {target_body['num']}-го тела"
                    answer_value = f"{m_target:.3f} кг"
                    explanation = "При тепловом равновесии Q_отданное = Q_полученное."
                    
                elif unknown == 'temperature':
                    target_body = bodies[-1]
                    other_bodies = bodies[:-1]
                    
                    # Используем заданную t_eq или вычисляем
                    t_eq_raw = request.form.get('t_eq', '').strip()
                    if t_eq_raw:
                        t_eq = float(t_eq_raw)
                        steps.append(f"Дано: t_равн = {t_eq:.2f} °C (задано)")
                    else:
                        t_eq = sum(b['c'] * b['mass'] * b['temp'] for b in other_bodies) / sum(b['c'] * b['mass'] for b in other_bodies)
                        steps.append(f"Находим t_равн: Σ(cᵢ·mᵢ·tᵢ) / Σ(cᵢ·mᵢ) = {t_eq:.2f} °C")
                    
                    numerator = sum(b['c'] * b['mass'] * (b['temp'] - t_eq) for b in other_bodies)
                    denominator = target_body['c'] * target_body['mass']
                    if denominator == 0:
                        raise ValueError("Деление на ноль")
                    t_target = t_eq - numerator / denominator
                    steps.append("Уравнение теплового баланса: Q_отданное = Q_полученное")
                    steps.append(f"t_{target_body['num']} = {t_target:.2f} °C")
                    answer_label = f"Температура {target_body['num']}-го тела"
                    answer_value = f"{t_target:.2f} °C"
                    explanation = "При тепловом равновесии все тела имеют одинаковую температуру."
                
                # unknown_label определяется по выбранной неизвестной
                if unknown == 't_eq':
                    unknown_label = 'Конечная температура'
                elif unknown == 'mass':
                    unknown_label = f"Масса {target_body['num']}-го тела"
                else:
                    unknown_label = f"Температура {target_body['num']}-го тела"
                
                for b in bodies:
                    bodies_info.append({
                        'name': f"Тело #{b['num']}",
                        'material': b['material'],
                        'material_name': material_names.get(b['material'], 'Пользовательский'),
                        'c': b['c'],
                        'mass': b['mass'],
                        'temp': b['temp']
                    })
            
            elif task_type == 'kinematics':
                task_type_name = 'Кинематика'
                v0 = request.form.get('v0', '').strip()
                a = request.form.get('a', '').strip()
                t = request.form.get('t', '').strip()
                S = request.form.get('S', '').strip()
                
                v0 = float(v0) if v0 else None
                a = float(a) if a else None
                t = float(t) if t else None
                S = float(S) if S else None
                
                filled = sum(1 for v in [v0, a, t, S] if v is not None)
                
                if filled < 2:
                    raise ValueError("Заполните минимум 2 поля")
                
                if v0 is None and a is not None and t is not None and S is not None:
                    v0 = (S - 0.5 * a * t**2) / t
                    steps.append(f"Находим v₀: S = v₀t + at²/2 → v₀ = (S - at²/2) / t")
                    steps.append(f"v₀ = ({S} - {a}·{t}²/2) / {t} = {v0:.2f} м/с")
                elif a is None and v0 is not None and t is not None and S is not None:
                    a = 2 * (S - v0 * t) / t**2
                    steps.append(f"Находим a: S = v₀t + at²/2 → a = 2(S - v₀t) / t²")
                    steps.append(f"a = 2({S} - {v0}·{t}) / {t}² = {a:.2f} м/с²")
                elif t is None and v0 is not None and a is not None and S is not None:
                    if a == 0:
                        t = S / v0 if v0 != 0 else 0
                    else:
                        D = v0**2 + 2*a*S
                        if D < 0:
                            raise ValueError("Дискриминант отрицательный")
                        t = (v0 + D**0.5) / a
                    steps.append(f"Находим t: S = v₀t + at²/2")
                    steps.append(f"t = {t:.2f} с")
                elif S is None and v0 is not None and a is not None and t is not None:
                    S = v0 * t + 0.5 * a * t**2
                    steps.append(f"Находим S: S = v₀t + at²/2")
                    steps.append(f"S = {v0}·{t} + 0.5·{a}·{t}² = {S:.2f} м")
                
                v = v0 + a * t if v0 is not None and a is not None and t is not None else None
                if v is not None:
                    steps.append(f"v = v₀ + at = {v0} + {a}·{t} = {v:.2f} м/с")
                
                answer_label = "Путь S"
                answer_value = f"{S:.2f} м"
                explanation = "Равноускоренное движение: S = v₀t + at²/2, v = v₀ + at"
            
            elif task_type == 'electricity':
                task_type_name = 'Закон Ома'
                I = request.form.get('I', '').strip()
                U = request.form.get('U', '').strip()
                R = request.form.get('R', '').strip()
                
                I = float(I) if I else None
                U = float(U) if U else None
                R = float(R) if R else None
                
                if I is None and U is not None and R is not None:
                    I = U / R
                    steps.append(f"Находим I: I = U / R = {U} / {R} = {I:.2f} А")
                elif U is None and I is not None and R is not None:
                    U = I * R
                    steps.append(f"Находим U: U = I · R = {I} · {R} = {U:.2f} В")
                elif R is None and I is not None and U is not None:
                    R = U / I
                    steps.append(f"Находим R: R = U / I = {U} / {I} = {R:.2f} Ом")
                
                P = U * I if U is not None and I is not None else None
                if P is not None:
                    steps.append(f"Мощность: P = U·I = {U}·{I} = {P:.2f} Вт")
                
                answer_label = "Мощность P"
                answer_value = f"{P:.2f} Вт" if P else ""
                explanation = "Закон Ома: U = I·R, мощность P = U·I"
            
            elif task_type == 'optics':
                task_type_name = 'Оптика — линза'
                d = request.form.get('d', '').strip()
                f = request.form.get('f', '').strip()
                
                d = float(d) if d else None
                f = float(f) if f else None
                
                if d is None and f is not None:
                    raise ValueError("Нужно ввести расстояние до предмета")
                if f is None and d is not None:
                    raise ValueError("Нужно ввести расстояние до изображения")
                
                F = 1 / (1/d + 1/f)
                steps.append(f"Формула тонкой линзы: 1/F = 1/d + 1/f")
                steps.append(f"1/F = 1/{d} + 1/{f} = {1/d:.4f} + {1/f:.4f} = {1/d + 1/f:.4f}")
                steps.append(f"F = {F:.2f}")
                
                D = 1 / F if F != 0 else 0
                steps.append(f"Оптическая сила: D = 1/F = {D:.2f} дптр")
                
                answer_label = "Фокусное расстояние"
                answer_value = f"{F:.2f}"
                explanation = "Формула тонкой линзы: 1/F = 1/d + 1/f"
        
        # ==================== МАТЕМАТИКА ====================
        elif category == 'math':
            if task_type == 'quadratic':
                task_type_name = 'Квадратное уравнение'
                a = float(request.form.get('a', '0') or '0')
                b = float(request.form.get('b', '0') or '0')
                c = float(request.form.get('c', '0') or '0')
                
                if a == 0:
                    raise ValueError("a не может быть 0 для квадратного уравнения")
                
                D = b**2 - 4*a*c
                steps.append(f"Дано: a={a}, b={b}, c={c}")
                steps.append(f"D = b² - 4ac = {b}² - 4·{a}·{c} = {D}")
                
                if D < 0:
                    steps.append("D < 0: корней нет")
                    answer_label = "Дискриминант"
                    answer_value = "Корней нет (D < 0)"
                    explanation = "Квадратное уравнение не имеет действительных корней"
                elif D == 0:
                    x = -b / (2*a)
                    steps.append(f"D = 0: x = -b/(2a) = {x:.2f}")
                    answer_label = "Корень"
                    answer_value = f"x = {x:.2f}"
                    explanation = "Квадратное уравнение имеет один корень"
                else:
                    x1 = (-b + D**0.5) / (2*a)
                    x2 = (-b - D**0.5) / (2*a)
                    steps.append(f"D > 0: два корня")
                    steps.append(f"x₁ = (-b + √D) / 2a = {x1:.2f}")
                    steps.append(f"x₂ = (-b - √D) / 2a = {x2:.2f}")
                    answer_label = "Корни"
                    answer_value = f"x₁ = {x1:.2f}, x₂ = {x2:.2f}"
                    explanation = "Квадратное уравнение имеет два корня"
            
            elif task_type == 'triangle_area':
                task_type_name = 'Площадь треугольника'
                a = float(request.form.get('a', '0') or '0')
                h = float(request.form.get('h', '0') or '0')
                S = 0.5 * a * h
                steps.append(f"Дано: a = {a}, h = {h}")
                steps.append(f"S = ½ · a · h = 0.5 · {a} · {h} = {S:.2f}")
                answer_label = "Площадь"
                answer_value = f"{S:.2f}"
                explanation = "Площадь треугольника: S = ½ah"
            
            elif task_type == 'trig':
                task_type_name = 'Тригонометрические функции'
                angle = float(request.form.get('angle', '0') or '0')
                angle_rad = math.radians(angle)
                sin_val = math.sin(angle_rad)
                cos_val = math.cos(angle_rad)
                tan_val = math.tan(angle_rad) if abs(math.cos(angle_rad)) > 1e-10 else None
                
                steps.append(f"Угол: {angle}° = {angle_rad:.4f} рад")
                steps.append(f"sin({angle}°) = {sin_val:.4f}")
                steps.append(f"cos({angle}°) = {cos_val:.4f}")
                if tan_val is not None:
                    steps.append(f"tan({angle}°) = {tan_val:.4f}")
                
                answer_label = "sin, cos, tan"
                answer_value = f"sin={sin_val:.4f}, cos={cos_val:.4f}"
                explanation = "Тригонометрические функции вычисляются по единичной окружности"
            
            elif task_type == 'derivative':
                task_type_name = 'Производная степени'
                n = float(request.form.get('n', '0') or '0')
                x = float(request.form.get('x', '0') or '0')
                
                if x == 0 and n - 1 < 0:
                    raise ValueError("Производная не определена в точке x = 0")
                
                deriv = n * (x ** (n - 1))
                steps.append(f"Дано: f(x) = x^{n}")
                steps.append(f"f'(x) = n · xⁿ⁻¹ = {n} · x^{n-1}")
                steps.append(f"f'({x}) = {n} · ({x})^{n-1} = {deriv:.4f}")
                answer_label = "f'(x)"
                answer_value = f"{deriv:.4f}"
                explanation = "Производная степени: d/dx(xⁿ) = n·xⁿ⁻¹"
            
            elif task_type == 'vector_add':
                task_type_name = 'Сложение векторов'
                va = float(request.form.get('va', '0') or '0')
                vb = float(request.form.get('vb', '0') or '0')
                vangle = float(request.form.get('vangle', '0') or '0')
                angle_rad = math.radians(vangle)
                
                result = (va**2 + vb**2 + 2*va*vb*math.cos(angle_rad))**0.5
                denominator = va + vb * math.cos(angle_rad)
                alpha = math.degrees(math.atan2(vb * math.sin(angle_rad), denominator)) if abs(denominator) > 1e-10 else 90.0
                
                steps.append(f"Дано: |a| = {va}, |b| = {vb}, γ = {vangle}°")
                steps.append(f"|a+b| = √(a²+b²+2ab·cos(γ))")
                steps.append(f"|a+b| = √{va**2 + vb**2 + 2*va*vb*math.cos(angle_rad):.4f} = {result:.2f}")
                steps.append(f"Угол α = {alpha:.2f}°")
                answer_label = "|a+b|"
                answer_value = f"{result:.2f}"
                explanation = "Сложение векторов по теореме косинусов"
            
            elif task_type == 'probability':
                task_type_name = 'Классическая вероятность'
                pm = int(float(request.form.get('pm', '0') or '0'))
                pn = int(float(request.form.get('pn', '1') or '1'))
                
                if pn == 0:
                    raise ValueError("n не может быть 0")
                if pm < 0 or pm > pn:
                    raise ValueError("m должно быть в диапазоне [0, n]")
                
                P = pm / pn
                percentage = P * 100
                steps.append(f"Дано: m = {pm}, n = {pn}")
                steps.append(f"P = m/n = {pm}/{pn} = {P:.4f}")
                steps.append(f"P = {percentage:.2f}%")
                answer_label = "Вероятность P"
                answer_value = f"{P:.4f} ({percentage:.2f}%)"
                explanation = "Классическая вероятность: P = m/n"
        
        # ==================== СОХРАНЕНИЕ ====================
        if not answer_value:
            answer_value = "Решение выполнено"
        
        inputs_str = ', '.join(f"{k}={request.form[k]}" for k in request.form if k not in ['category', 'task_type', 'unknown'])
        results_str = f"{answer_label}={answer_value}"
        save_solution(user['id'], f'builder_{task_type}', task_type_name, inputs_str, results_str)
        add_xp(user['id'], 15)
        add_coins(user['id'], 10)
        
        return render_template(
            'result_builder.html',
            task_type_name=task_type_name,
            bodies_info=bodies_info,
            steps=steps,
            explanation=explanation,
            answer_label=answer_label,
            answer_value=answer_value,
            unknown_label=unknown_label,
            graph_svg=None
        )
    
    except Exception as e:
        return render_template(
            'result_builder.html',
            error=f"Ошибка расчёта: {str(e)}",
            task_type_name="",
            bodies_info=[],
            steps=[],
            explanation="",
            answer_label="",
            answer_value="",
            unknown_label="",
            graph_svg=None
        )


# ==================== ПРОФИЛЬ ====================

@app.route('/profile')
def profile():
    user = get_current_user()
    if not user:
        flash('Войдите в аккаунт', 'warning')
        return redirect(url_for('login'))
    
    records = get_history(user['id'])
    return render_template('profile.html', user=user, history=records)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
