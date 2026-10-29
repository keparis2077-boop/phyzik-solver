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
            "quantities": quantities,
            "targets": targets,
            "solve": _build_solve_function(tmpl),
        }

    return tasks


def _infer_category(task_id: str) -> str:
    """Выводит категорию из task_id, если не указана в spec."""
    category_map = {
        "kinematics": "Кинематика",
        "freefall": "Кинематика",
        "ballistics": "Кинематика",
        "newton": "Динамика",
        "gravity": "Динамика",
        "ohm": "Электричество",
        "series": "Электричество",
        "parallel": "Электричество",
        "work": "Энергия",
        "energy": "Энергия",
        "power": "Энергия",
        "pressure": "Давление",
        "density": "Давление",
        "archimedes": "Давление",
        "heat": "Термодинамика",
        "reflection": "Оптика",
    }
    return category_map.get(task_id, "Прочее")


# ─── Глобальная переменная TASKS ───────────────────────────────
# Загружается при старте приложения

TASKS = build_tasks_dict()


def group_by_category() -> dict:
    """Группирует задачи по категориям для главной страницы."""
    groups = {}
    for tid, t in TASKS.items():
        cat = t.get("category", "Прочее")
        groups.setdefault(cat, []).append((tid, t))
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
