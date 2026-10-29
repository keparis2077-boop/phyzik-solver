# app.py
import json
from flask import Flask, render_template, request, redirect, url_for, flash
from loader import TASKS, group_by_category
from reference import CONSTANTS, FORMULAS
from database import init_db, save_solution, get_history, clear_history

app = Flask(__name__)
app.secret_key = 'change-me-in-production'
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


@app.route('/')
def index():
    return render_template('index.html',
                           groups=group_by_category(),
                           total=len(TASKS))


@app.route('/task/<task_id>')
def task(task_id):
    if task_id not in TASKS:
        return redirect(url_for('index'))
    return render_template('task.html', task_id=task_id, task=TASKS[task_id])


@app.route('/solve/<task_id>', methods=['POST'])
def solve(task_id):
    if task_id not in TASKS:
        return redirect(url_for('index'))

    t = TASKS[task_id]

    # --- Новый режим: выбор неизвестной (есть поле quantities) ---
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
            save_solution(task_id, t['name'], inputs_str, results_str)
        except Exception as e:
            results, steps, explanation = {}, [], ''
            error = str(e)

        return render_template(
            'result.html',
            task_id=task_id, task=t,
            results=results, steps=steps, explanation=explanation,
            error=error, form=request.form,
        )

    # --- Старый режим: inputs + outputs (для остальных 12 задач) ---
    selected = request.form.getlist('outputs') or list(t.get('outputs', {}).keys())
    try:
        results, steps, explanation = t['solve'](request.form, selected)
        error = None
        inputs_str = ', '.join(
            f"{label.split('(')[0].strip()}={request.form[key]} {unit}"
            for key, label, unit in t['inputs']
        )
        results_str = '; '.join(f"{k}: {v}" for k, v in results.items())
        save_solution(task_id, t['name'], inputs_str, results_str)
    except Exception as e:
        results, steps, explanation = {}, [], ""
        error = f"Ошибка ввода: {e}"

    return render_template(
        'result.html',
        task_id=task_id, task=t,
        results=results, steps=steps, explanation=explanation,
        error=error, form=request.form,
    )


@app.route('/history')
def history():
    records = get_history()
    return render_template('history.html', records=records)


@app.route('/history/clear', methods=['POST'])
def history_clear():
    clear_history()
    flash('История очищена', 'success')
    return redirect(url_for('history'))


@app.route('/reference')
def reference():
    return render_template('reference.html', constants=CONSTANTS, formulas=FORMULAS)

if __name__ == '__main__':
    app.run(debug=True)