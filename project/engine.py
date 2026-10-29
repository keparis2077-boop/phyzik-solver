"""
Engine — универсальный решатель задач по спецификациям.
Читает spec, валидирует входные данные, вычисляет результат,
генерирует пошаговое решение.
"""

import math
import re
from pathlib import Path
from typing import Any

import yaml


# ─── Константы, общие для всех задач ──────────────────────────
PHYSICS_CONSTANTS = {
    "g": 9.8,
}


def _resolve_constant(name: str) -> float:
    """Возвращает значение физической константы."""
    if name in PHYSICS_CONSTANTS:
        return PHYSICS_CONSTANTS[name]
    raise ValueError(f"Неизвестная константа: {name}")


def _eval_expression(expr: str, known: dict) -> float:
    """
    Вычисляет выражение (например 'R1 + R2' или 'F = m * a') в контексте known.
    Если есть '=', берёт только правую часть.
    Поддерживает: +, -, *, /, **, math.*, sin, cos, tan, sqrt, radians.
    """
    # Если формула содержит '=', берём только правую часть
    if "=" in expr:
        expr = expr.split("=", 1)[1].strip()

    namespace = dict(known)
    namespace.update(math.__dict__)
    namespace.update({
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "radians": math.radians,
        "pi": math.pi,
    })

    # Добавляем константы
    for name, val in PHYSICS_CONSTANTS.items():
        namespace[name] = val

    return eval(expr, {"__builtins__": {}}, namespace)


def _format_value(value: float, precision: str = ".3f") -> str:
    """Форматирует число с указанным количеством знаков."""
    return f"{value:{precision}}"


def _fill_steps(steps: list, known: dict, result: float) -> list:
    """
    Подставляет значения переменных в шаги решения.
    Пример: "v = {v0} + {a}·{t} = {result:.3f} м/с"
    """
    filled = []
    for step in steps:
        # Подставляем известные переменные
        for key, val in known.items():
            step = step.replace(f"{{{key}}}", str(val))
        # Подставляем результат с точностью
        match = re.search(r"\{result:([.\d]+f)\}", step)
        if match:
            precision = match.group(1)
            step = step.replace(match.group(0), _format_value(result, precision))
        else:
            step = step.replace("{result}", str(result))
        filled.append(step)
    return filled


def _validate_constraints(constraints: list, known: dict) -> str | None:
    """
    Проверяет ограничения (constraints).
    Возвращает сообщение об ошибке или None.
    """
    for c in constraints:
        field = c.get("field")
        expression = c.get("expression", field)
        condition = c["condition"]
        value = c["value"]

        # Вычисляем выражение или берём переменную
        try:
            actual = _eval_expression(expression, known)
        except Exception:
            actual = known.get(expression, 0)

        # Проверяем условие
        if condition == "!=" and actual == value:
            return f"Деление на ноль: {expression} не может быть равно {value}"
        if condition == ">=" and actual < value:
            return f"Нет решения: {expression} = {actual} < {value}"
        if condition == ">" and actual <= value:
            return f"Нет решения: {expression} = {actual} ≤ {value}"
        if condition == "==" and actual != value:
            return f"Условие не выполнено: {expression} ≠ {value}"

    return None


def solve_task(template: dict, inputs: dict, target: str) -> tuple[dict, list, str]:
    """
    Решает задачу по спецификации.

    Args:
        template: шаблон из YAML-спецификации
        inputs: словарь {переменная: значение} для известных величин
        target: какая величина ищется

    Returns:
        (results, steps, explanation)
    """
    variables = template.get("variables", {})
    solutions = template.get("solutions", [])
    explanation = template.get("explanation", "")

    # Находим подходящее решение для этого target
    solution = None
    for sol in solutions:
        if sol["target"] == target:
            required = set(sol["requires"])
            input_keys = set(inputs.keys())

            # Проверяем, что все required переменные есть во вводе
            # (кроме самой искомой)
            if required.issubset(input_keys):
                solution = sol
                break

    if solution is None:
        raise ValueError(
            f"Не удалось найти решение для target={target}. "
            f"Введены: {list(inputs.keys())}. "
            f"Нужны: {list(solution['requires']) if solution else '—'}"
        )

    # Вычисляем результат
    formula = solution["formula"]
    try:
        result_value = _eval_expression(formula, inputs)
    except Exception as e:
        raise ValueError(f"Ошибка вычисления: {e}")

    # Проверяем constraints
    constraints = solution.get("constraints", [])
    if constraints:
        error = _validate_constraints(constraints, inputs)
        if error:
            raise ValueError(error)

    # Проверяем validation (например, дискриминант >= 0)
    validations = solution.get("validation", [])
    for v in validations:
        try:
            actual = _eval_expression(v["expression"], inputs)
        except Exception:
            actual = inputs.get(v["expression"], 0)

        if v["condition"] == ">=" and actual < v["value"]:
            raise ValueError(v.get("error", f"Нет решения: {v['expression']} < 0"))
        if v["condition"] == ">" and actual <= v["value"]:
            raise ValueError(v.get("error", f"Нет решения: {v['expression']} ≤ 0"))

    # Формируем шаги
    steps = _fill_steps(solution["steps"], inputs, result_value)

    # Форматируем результат с единицами измерения
    target_var = variables.get(target, {})
    unit = target_var.get("unit", "")
    result_key = target
    result_str = f"{_format_value(result_value)} {unit}".strip()

    return {result_key: result_str}, steps, explanation


# ─── Загрузка спецификаций ─────────────────────────────────────

def load_specs(specs_dir: str | Path = None) -> dict:
    """
    Загружает все YAML-спецификации из директории specs/.

    Returns:
        dict {task_id: template_dict} — готовый для Flask словарь TASKS
    """
    if specs_dir is None:
        specs_dir = Path(__file__).parent / "specs"
    else:
        specs_dir = Path(specs_dir)

    tasks = {}

    for spec_file in sorted(specs_dir.glob("*.yaml")):
        with open(spec_file, "r", encoding="utf-8") as f:
            spec_data = yaml.safe_load(f)

        templates = spec_data.get("templates", [])
        for tmpl in templates:
            task_id = tmpl["id"]
            tasks[task_id] = tmpl

    return tasks


# ─── Валидация спецификаций ────────────────────────────────────

def validate_specs(specs_dir: str | Path = None) -> list[str]:
    """
    Проверяет корректность всех спецификаций.
    Возвращает список сообщений об ошибках (пусто — всё ОК).
    """
    errors = []
    tasks = {}

    if specs_dir is None:
        specs_dir = Path(__file__).parent / "specs"

    for spec_file in sorted(specs_dir.glob("*.yaml")):
        with open(spec_file, "r", encoding="utf-8") as f:
            spec_data = yaml.safe_load(f)

        templates = spec_data.get("templates", [])
        for tmpl in templates:
            task_id = tmpl.get("id")
            if not task_id:
                errors.append(f"{spec_file}: нет id у шаблона")
                continue

            if task_id in tasks:
                errors.append(f"{spec_file}: дубликат id '{task_id}'")
                continue

            tasks[task_id] = tmpl

            # Проверяем обязательные поля
            if not tmpl.get("name"):
                errors.append(f"{task_id}: нет name")
            if not tmpl.get("variables"):
                errors.append(f"{task_id}: нет variables")
            if not tmpl.get("solutions"):
                errors.append(f"{task_id}: нет solutions")

            # Проверяем решения
            if tmpl.get("solutions"):
                for sol in tmpl["solutions"]:
                    if not sol.get("target"):
                        errors.append(f"{task_id}.{sol.get('id', '?')}: нет target")
                    if not sol.get("requires"):
                        errors.append(f"{task_id}.{sol.get('id', '?')}: нет requires")
                    if not sol.get("formula"):
                        errors.append(f"{task_id}.{sol.get('id', '?')}: нет formula")

                    # Проверяем, что все required переменные объявлены
                    for req in sol["requires"]:
                        if req not in tmpl["variables"]:
                            errors.append(
                                f"{task_id}.{sol['id']}: requires '{req}' "
                                f"не объявлен в variables"
                            )

    return errors
