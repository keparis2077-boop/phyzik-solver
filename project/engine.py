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
        "degrees": math.degrees,
        "pi": math.pi,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "log": math.log,
        "log2": math.log2,
        "exp": math.exp,
        "e": math.e,
    })

    # Добавляем константы
    for name, val in PHYSICS_CONSTANTS.items():
        namespace[name] = val

    return eval(expr, {"__builtins__": {}}, namespace)


def _format_value(value: float, precision: str = ".3f") -> str:
    """Форматирует число с указанным количеством знаков."""
    return f"{value:{precision}}"


def _get_exact_trig(angle_deg: float) -> tuple[str, float] | None:
    """
    Возвращает точное значение тригонометрической функции для специальных углов.
    Returns: (строка с корнем, десятичное значение) или None.
    """
    special_angles = {
        0:   {"sin": ("0", 0.0), "cos": ("1", 1.0), "tan": ("0", 0.0)},
        30:  {"sin": ("1/2", 0.5), "cos": ("√3/2", 0.8660254), "tan": ("√3/3", 0.5773503)},
        45:  {"sin": ("√2/2", 0.7071068), "cos": ("√2/2", 0.7071068), "tan": ("1", 1.0)},
        60:  {"sin": ("√3/2", 0.8660254), "cos": ("1/2", 0.5), "tan": ("√3", 1.7320508)},
        90:  {"sin": ("1", 1.0), "cos": ("0", 0.0), "tan": None},
        120: {"sin": ("√3/2", 0.8660254), "cos": ("-1/2", -0.5), "tan": ("-√3", -1.7320508)},
        135: {"sin": ("√2/2", 0.7071068), "cos": ("-√2/2", -0.7071068), "tan": ("-1", -1.0)},
        150: {"sin": ("1/2", 0.5), "cos": ("-√3/2", -0.8660254), "tan": ("-√3/3", -0.5773503)},
        180: {"sin": ("0", 0.0), "cos": ("-1", -1.0), "tan": ("0", 0.0)},
    }
    angle = round(angle_deg)
    if angle in special_angles:
        return special_angles[angle]
    return None


def _format_trig_in_step(step: str, known: dict) -> str:
    """
    Ищет в шаге sin(α°), cos(α°), tan(α°) и подставляет точные значения с корнями.
    Также обрабатывает sin(α) без градусов — для шагов из YAML.
    """
    import re

    # Сначала заменяем sin(radians(α)), cos(radians(α)), tan(radians(α))
    def replace_trig_radians(match):
        func = match.group(1)
        angle = float(match.group(2))
        exact = _get_exact_trig(angle)
        if exact and func in exact:
            return exact[func][0]
        try:
            rad = math.radians(angle)
            if func == "sin":
                return str(round(math.sin(rad), 6))
            elif func == "cos":
                return str(round(math.cos(rad), 6))
            elif func == "tan":
                val = math.tan(rad)
                if abs(val) > 1e10:
                    return "∞"
                return str(round(val, 6))
        except Exception:
            pass
        return match.group(0)

    step = re.sub(r'(sin|cos|tan)\(radians\((\d+(?:\.\d+)?)\)\)', replace_trig_radians, step)

    # Заменяем sin(α°), cos(α°), tan(α°)
    pattern = r'(sin|cos|tan)\((\d+(?:\.\d+)?)°?\)'

    def replace_trig(match):
        func = match.group(1)
        angle = float(match.group(2))
        exact = _get_exact_trig(angle)
        if exact and func in exact:
            return exact[func][0]
        try:
            rad = math.radians(angle)
            if func == "sin":
                return str(round(math.sin(rad), 6))
            elif func == "cos":
                return str(round(math.cos(rad), 6))
            elif func == "tan":
                val = math.tan(rad)
                if abs(val) > 1e10:
                    return "∞"
                return str(round(val, 6))
        except Exception:
            pass
        return match.group(0)

    return re.sub(pattern, replace_trig, step)


def _format_num_for_exact(val: float) -> str:
    """Форматирует число для точного выражения."""
    if val == int(val):
        return str(int(val))
    return str(val)


def _build_exact_expression(solution: dict, known: dict, result_value: float) -> str:
    """
    Строит точное выражение результата из формулы и известных значений.
    Заменяет sin(radians(45)) на √2/2, cos(radians(30)) на √3/2 и т.д.
    """
    formula = solution["formula"]
    # Если формула содержит '=', берём только правую часть
    if "=" in formula:
        formula = formula.split("=", 1)[1].strip()

    # Сначала заменяем переменные внутри trig/radians функций
    for key, val in known.items():
        num_str = _format_num_for_exact(val)
        # Заменяем radians(key) -> radians(num) без лишних скобок
        formula = formula.replace(f"radians({key})", f"radians({num_str})")
        # Заменяем sin(key) -> sin(num), cos(key) -> cos(num), tan(key) -> tan(num)
        formula = formula.replace(f"sin({key})", f"sin({num_str})")
        formula = formula.replace(f"cos({key})", f"cos({num_str})")
        formula = formula.replace(f"tan({key})", f"tan({num_str})")

    # Заменяем оставшиеся переменные (с скобками)
    for key, val in known.items():
        num_str = _format_num_for_exact(val)
        formula = formula.replace(key, f"({num_str})")

    # Заменяем sin(radians(α)), cos(radians(α)), tan(radians(α)) на точные значения
    def replace_trig_exact(match):
        func = match.group(1)
        angle = float(match.group(2))
        exact = _get_exact_trig(angle)
        if exact and func in exact and exact[func] is not None:
            return exact[func][0]
        return match.group(0)

    # Сначала заменяем sin(radians(45)), cos(radians(45)), tan(radians(45))
    formula = re.sub(r'(sin|cos|tan)\(radians\((\d+(?:\.\d+)?)\)\)', replace_trig_exact, formula)
    # Затем заменяем sin(45°), cos(45°), tan(45°)
    formula = re.sub(r'(sin|cos|tan)\((\d+(?:\.\d+)?)°?\)', replace_trig_exact, formula)

    # Заменяем константы
    for name, val in PHYSICS_CONSTANTS.items():
        formula = formula.replace(name, f"({val})")

    # Убираем лишние скобки вокруг чисел
    formula = re.sub(r'\((\d+\.?\d*)\)', r'\1', formula)
    formula = re.sub(r'\((\d+\.?\d*)\)', r'\1', formula)  # дважды для вложенных

    return formula


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
        # Заменяем sin(45°), cos(30°) и т.д. на точные значения с корнями
        step = _format_trig_in_step(step, known)
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
    required_vars = []
    for sol in solutions:
        if sol["target"] == target:
            required = set(sol["requires"])
            required_vars = list(required)
            input_keys = set(inputs.keys())

            # Проверяем, что все required переменные есть во вводе
            # (кроме самой искомой)
            if required.issubset(input_keys):
                solution = sol
                break

    if solution is None:
        missing = [v for v in required_vars if v not in inputs]
        raise ValueError(
            f"Недостаточно данных для target={target}. "
            f"Введены: {list(inputs.keys())}. "
            f"Не хватает: {missing if missing else required_vars}"
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
    result_num = _format_value(result_value)
    result_str = f"{result_num} {unit}".strip()

    # Формируем точное выражение результата с единицами
    try:
        exact_str = _build_exact_expression(solution, inputs, result_value)
        if exact_str and unit:
            exact_str = f"{exact_str} {unit}"
    except Exception:
        exact_str = ""

    # Возвращаем число и единицу отдельно
    return {result_key: result_num, "_unit": unit}, steps, explanation, exact_str, unit


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
