# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from loader import TASKS, group_by_category
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
    return render_template('index.html',
                           groups=group_by_category(),
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
    return render_template('reference.html', constants=CONSTANTS, formulas=FORMULAS)


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
    
    return render_template('math.html',
                           algebra_tasks=algebra_tasks,
                           geometry_tasks=geometry_tasks,
                           trigonometry_tasks=trigonometry_tasks)


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
    
    task_type = request.form.get('task_type', 'thermal_balance')
    unknown = request.form.get('unknown', 't_eq')
    
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
            task_type_name="",
            bodies_info=[],
            steps=[],
            explanation="",
            answer_label="",
            answer_value="",
            graph_svg=None
        )
    
    material_names = {
        'water': 'Вода', 'ice': 'Лёд', 'aluminum': 'Алюминий',
        'iron': 'Железо', 'copper': 'Медь', 'lead': 'Свинец',
        'custom': 'Пользовательский'
    }
    
    steps = []
    explanation = ""
    answer_label = ""
    answer_value = ""
    
    try:
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
            
            t_eq = sum(b['c'] * b['mass'] * b['temp'] for b in other_bodies) / sum(b['c'] * b['mass'] for b in other_bodies)
            
            numerator = sum(b['c'] * b['mass'] * (t_eq - b['temp']) for b in other_bodies)
            denominator = target_body['c'] * (target_body['temp'] - t_eq)
            
            if denominator == 0:
                raise ValueError("Деление на ноль")
            
            m_target = numerator / denominator
            
            steps.append("Уравнение теплового баланса: Q_отданное = Q_полученное")
            steps.append(f"t_равн = {t_eq:.2f} °C")
            steps.append(f"m_{target_body['num']} = {m_target:.3f} кг")
            answer_label = f"Масса {target_body['num']}-го тела"
            answer_value = f"{m_target:.3f} кг"
            explanation = "При тепловом равновесии Q_отданное = Q_полученное."
            
        elif unknown == 'temperature':
            target_body = bodies[-1]
            other_bodies = bodies[:-1]
            
            t_eq = sum(b['c'] * b['mass'] * b['temp'] for b in other_bodies) / sum(b['c'] * b['mass'] for b in other_bodies)
            
            numerator = sum(b['c'] * b['mass'] * (b['temp'] - t_eq) for b in other_bodies)
            denominator = target_body['c'] * target_body['mass']
            
            if denominator == 0:
                raise ValueError("Деление на ноль")
            
            t_target = t_eq - numerator / denominator
            
            steps.append("Уравнение теплового баланса: Q_отданное = Q_полученное")
            steps.append(f"t_равн = {t_eq:.2f} °C")
            steps.append(f"t_{target_body['num']} = {t_target:.2f} °C")
            answer_label = f"Температура {target_body['num']}-го тела"
            answer_value = f"{t_target:.2f} °C"
            explanation = "При тепловом равновесии все тела имеют одинаковую температуру."
        
        task_type_names = {
            'thermal_balance': 'Тепловое равновесие',
            'mixing': 'Смешивание жидкостей',
            'ice_melting': 'Плавление льда'
        }
        
        unknown_labels = {
            't_eq': 'Конечная температура',
            'mass': f"Масса {target_body['num']}-го тела",
            'temperature': f"Температура {target_body['num']}-го тела"
        }
        
        bodies_info = []
        for b in bodies:
            bodies_info.append({
                'name': f"Тело #{b['num']}",
                'material': b['material'],
                'material_name': material_names.get(b['material'], 'Пользовательский'),
                'c': b['c'],
                'mass': b['mass'],
                'temp': b['temp']
            })
        
        return render_template(
            'result_builder.html',
            task_type_name=task_type_names.get(task_type, 'Конструктор'),
            bodies_info=bodies_info,
            steps=steps,
            explanation=explanation,
            answer_label=answer_label,
            answer_value=answer_value,
            unknown_label=unknown_labels.get(unknown, 'Неизвестная величина'),
            graph_svg=None
        )
        
    except Exception as e:
        return render_template(
            'result_builder.html',
            error=f"Ошибка расчёта: {str(e)}",
            task_type_name="",
            bodies_info=bodies,
            steps=[],
            explanation="",
            answer_label="",
            answer_value="",
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
