"""
loader.py — загрузчик спецификаций для Flask-приложения.
Заменяет старый tasks.py.

Использование:
    from loader import TASKS, group_by_category

    # TASKS — словарь, совместимый со старым tasks.py
    # {task_id: {name, category, icon, image, quantities, targets, solve}}
"""

from engine import load_specs, validate_specs, solve_task
from pathlib import Path


def _build_solve_function(template: dict):
    """
    Создаёт функцию solve() для Flask, которая вызывает engine.solve_task().
    Совместима со старым интерфейсом: solve(known, target) -> (results, steps, explanation)
    """
    def solve(known: dict, target: str):
        return solve_task(template, known, target)
    return solve


def build_tasks_dict() -> dict:
    """
    Загружает YAML-спецификации и формирует словарь TASKS
    в формате, совместимом с текущим app.py.
    """
    specs_dir = Path(__file__).parent / "specs"
    templates = load_specs(specs_dir)
    tasks = {}

    for task_id, tmpl in templates.items():
        variables = tmpl["variables"]

        # Формируем quantities для шаблона формы
        quantities = {}
        for key, var in variables.items():
            quantities[key] = (var["label"], var["unit"])

        # Формируем targets для выпадающего списка
        targets = {}
        for sol in tmpl["solutions"]:
            target_key = sol["target"]
            # Проверяем, нет ли уже такой записи
            if target_key not in targets:
                targets[target_key] = sol.get("label", f"Найти {target_key}")

        tasks[task_id] = {
            "name": tmpl["name"],
            "category": tmpl.get("category", _infer_category(task_id)),
            "icon": tmpl.get("icon", "📐"),
            "image": tmpl.get("image", ""),
            "condition": tmpl.get("description", tmpl.get("condition", "Решите задачу")),
            "difficulty": tmpl.get("difficulty", _infer_difficulty(task_id)),
            "quantities": quantities,
            "targets": targets,
            "solve": _build_solve_function(tmpl),
            "graph_type": tmpl.get("graph_type", _infer_graph_type(task_id)),
        }

    return tasks


def _infer_category(task_id: str) -> str:
    """Выводит категорию из task_id, если не указана в spec."""
    category_map = {
        # Кинематика
        "kinematics": "Кинематика",
        "freefall": "Кинематика",
        "ballistics": "Кинематика",
        # Динамика
        "newton": "Динамика",
        "gravity": "Динамика",
        "forces": "Динамика",
        "momentum": "Динамика",
        "weight": "Динамика",
        "friction": "Динамика",
        "elastic": "Динамика",
        # Механика 7 класс
        "uniform_motion": "Механика",
        "average_speed": "Механика",
        "density": "Механика",
        # Электричество
        "ohm": "Электричество",
        "series": "Электричество",
        "parallel": "Электричество",
        "electric_power": "Электричество",
        # Энергия
        "work": "Энергия",
        "energy": "Энергия",
        "power": "Энергия",
        # Давление
        "pressure": "Давление",
        "archimedes": "Давление",
        # Тепловые явления 8 класс
        "heat_capacity": "Тепловые явления",
        "melting": "Тепловые явления",
        "vaporization": "Тепловые явления",
        "fuel_combustion": "Тепловые явления",
        # Термодинамика
        "heat": "Термодинамика",
        "ideal_gas": "Молекулярная физика",
        "clausius_clapeyron": "Молекулярная физика",
        "humidity": "Молекулярная физика",
        # Оптика
        "reflection": "Оптика",
        "refraction": "Оптика",
        "thin_lens": "Оптика",
        "optical_power": "Оптика",
        # Колебания
        "oscillations": "Колебания и волны",
        "frequency": "Колебания и волны",
        "wave": "Колебания и волны",
        "pendulum": "Колебания и волны",
        "spring_pendulum": "Колебания и волны",
        # Квантовая физика
        "quantum": "Квантовая физика",
        "photon_energy": "Квантовая физика",
        "photoelectric": "Квантовая физика",
        "de_broglie": "Квантовая физика",
        # Ядерная физика
        "nuclear": "Ядерная физика",
        "mass_energy": "Ядерная физика",
        "binding_energy": "Ядерная физика",
        "radioactivity": "Ядерная физика",
        # Электромагнетизм
        "electromagnetism": "Электромагнетизм",
        "lorentz_force": "Электромагнетизм",
        "ampere_force": "Электромагнетизм",
        "electromagnetic_wave": "Электромагнетизм",
        "inductance": "Электромагнетизм",
        # Математика
        "math": "Математика",
    }
    return category_map.get(task_id, "Прочее")


def _infer_difficulty(task_id: str) -> str:
    """Выводит сложность (класс) из task_id."""
    difficulty_map = {
        # 7 класс
        "uniform_motion": "7",
        "average_speed": "7",
        "density": "7",
        "pressure": "7",
        "reflection": "7",
        "heat_capacity": "8",
        "melting": "8",
        "vaporization": "8",
        "fuel_combustion": "8",
        # 8-9 класс
        "freefall": "9",
        "ballistics": "9",
        "newton": "9",
        "gravity": "9",
        "friction": "9",
        "elastic": "9",
        "ohm": "9",
        "series": "9",
        "parallel": "9",
        "electric_power": "9",
        "work": "9",
        "energy": "9",
        "power": "9",
        "archimedes": "9",
        "refraction": "9",
        "oscillations": "9",
        "frequency": "9",
        "wave": "9",
        "pendulum": "9",
        # 10 класс
        "kinematics": "10",
        "momentum": "10",
        "weight": "10",
        "heat": "10",
        "ideal_gas": "10",
        "clausius_clapeyron": "10",
        "humidity": "10",
        "thin_lens": "10",
        "optical_power": "10",
        "spring_pendulum": "10",
        "quantum": "11",
        "photon_energy": "11",
        "photoelectric": "11",
        "de_broglie": "11",
        # 11 класс
        "nuclear": "11",
        "mass_energy": "11",
        "binding_energy": "11",
        "radioactivity": "11",
        "electromagnetism": "11",
        "lorentz_force": "11",
        "ampere_force": "11",
        "electromagnetic_wave": "11",
        "inductance": "11",
    }
    return difficulty_map.get(task_id, "9")


def _infer_graph_type(task_id: str) -> str:
    """Выводит тип графика из task_id."""
    graph_map = {
        "kinematics": "kinematics",
        "freefall": "freefall",
        "ballistics": "ballistics",
        "newton": "newton",
        "gravity": "newton",
        "ohm": "ohm",
        "series": "ohm",
        "parallel": "ohm",
        "work": "energy",
        "energy": "energy",
        "power": "power",
        "pressure": "pressure",
        "density": "pressure",
        "archimedes": "pressure",
        "heat": "heat",
        "lens": "lens",
        "optical_power": "lens",
        "magnification": "lens",
    }
    return graph_map.get(task_id, None)


# ─── Глобальная переменная TASKS ───────────────────────────────
# Загружается при старте приложения

TASKS = build_tasks_dict()


CATEGORY_COLORS = {
    "Кинематика": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "Динамика": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
    "Электричество": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
    "Энергия": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
    "Давление": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
    "Термодинамика": "linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)",
    "Оптика": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",
}


def group_by_category() -> dict:
    """Группирует задачи по категориям для главной страницы."""
    groups = {}
    for tid, t in TASKS.items():
        cat = t.get("category", "Прочее")
        t_copy = dict(t)
        t_copy["color"] = CATEGORY_COLORS.get(cat, "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
        groups.setdefault(cat, []).append((tid, t_copy))
    return groups


def get_math_tasks_by_category() -> dict:
    """Получает математические задачи, сгруппированные по категориям."""
    math_categories = {'Алгебра', 'Геометрия', 'Тригонометрия', 'Анализ', 'Векторы', 'Теория вероятностей'}
    groups = {}
    for tid, t in TASKS.items():
        cat = t.get("category", "Прочее")
        if cat in math_categories:
            t_copy = dict(t)
            t_copy["color"] = CATEGORY_COLORS.get(cat, "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")
            t_copy["id"] = tid
            groups.setdefault(cat, []).append((tid, t_copy))
    return groups


# ─── Проверка при импорте ──────────────────────────────────────
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    errors = validate_specs()
    if errors:
        print("Ошибки в спецификациях:")
        for e in errors:
            print(f"  - {e}")
    else:
        print(f"Все спецификации валидны ({len(TASKS)} задач)")
        print("\nЗагруженные задачи:")
        for tid, t in TASKS.items():
            print(f"  [{t['category']}] {t['icon']} {t['name']} "
                  f"({len(t['quantities'])} величин, {len(t['targets'])} решений)")