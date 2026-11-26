"""
Решатель неравенств на основе sympy.
Поддерживает: линейные, квадратичные, рациональные, иррациональные неравенства.
"""

from sympy import (
    symbols, solve_univariate_inequality, Ge, Gt, Le, Lt,
    Poly, factor, simplify, expand, sqrt, Rational,
    S, Interval, Union, And, Or,
    sympify, SympifyError,
)
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application,
    convert_xor, function_exponentiation,
)

PARSING_TRANSFORMATIONS = (
    standard_transformations +
    (implicit_multiplication_application, convert_xor, function_exponentiation)
)


def parse_expr_user(expr_str: str):
    """Парсит выражение пользователя."""
    s = expr_str.strip().replace('^', '**')
    try:
        return parse_expr(
            s,
            local_dict={'pi': 3.14159265358979, 'sqrt': sqrt},
            transformations=PARSING_TRANSFORMATIONS,
            evaluate=True,
        )
    except (SympifyError, Exception):
        raise ValueError(f"Не удалось распознать выражение: '{expr_str}'")


def format_interval(interval):
    """Форматирует интервал sympy в красивую строку."""
    if interval is S.EmptySet:
        return "нет решений"
    
    if isinstance(interval, Interval):
        left, right = interval.inf, interval.sup
        left_open = interval.left_open
        right_open = interval.right_open
        
        left_str = format_endpoint(left, left_open)
        right_str = format_endpoint(right, right_open)
        
        return f"[{left_str}, {right_str}]" if not (left_open or right_open) else f"({left_str}, {right_str})"
    
    if isinstance(interval, Union):
        # Union of intervals
        intervals = []
        for arg in interval.args:
            if isinstance(arg, Interval):
                intervals.append(format_interval(arg))
        return " ∪ ".join(intervals) if intervals else "нет решений"
    
    return str(interval)


def format_endpoint(value, is_open):
    """Форматирует конечную точку интервала."""
    if value is S.NegativeInfinity:
        return "-∞"
    if value is S.Infinity:
        return "+∞"
    
    try:
        val = float(value.evalf())
        if val == int(val):
            return str(int(val))
        else:
            return f"{val:.4f}".rstrip('0')
    except (TypeError, ValueError):
        return str(value)


def solve_linear_inequality(expr_str: str, variable: str = 'x'):
    """
    Решает линейное неравенство вида: ax + b > 0, ax + b < c, и т.д.
    
    Returns:
        dict с решениями и шагами
    """
    steps = []
    var = symbols(variable)
    
    steps.append(f"Исходное неравенство: {expr_str}")
    
    # Парсим
    try:
        left = parse_expr_user(expr_str.split('>')[0].split('<')[0].split('≥')[0].split('≤')[0].strip())
    except ValueError as e:
        raise ValueError(str(e))
    
    # Определяем знак неравенства
    op = '>'
    if '<' in expr_str:
        op = '<'
    elif '≥' in expr_str or '>=' in expr_str:
        op = '≥'
    elif '≤' in expr_str or '<=' in expr_str:
        op = '≤'
    
    # Определяем правую часть
    if '>' in expr_str:
        right_str = expr_str.split('>')[1].strip()
    elif '<' in expr_str:
        right_str = expr_str.split('<')[1].strip()
    elif '≥' in expr_str or '>=' in expr_str:
        right_str = expr_str.split('≥')[1].strip() if '≥' in expr_str else expr_str.split('>=')[1].strip()
    elif '≤' in expr_str or '<=' in expr_str:
        right_str = expr_str.split('≤')[1].strip() if '≤' in expr_str else expr_str.split('<=')[1].strip()
    else:
        right_str = '0'
    
    right = parse_expr_user(right_str)
    
    # Переносим всё влево
    expr = simplify(left - right)
    expanded = expand(expr)
    steps.append(f"Переносим всё влево: {expanded} {op} 0")
    
    # Получаем коэффициенты
    poly = Poly(expanded, var)
    degree = poly.degree()
    coeffs = poly.all_coeffs()
    
    if degree != 1:
        raise ValueError("Это не линейное неравенство")
    
    a, b = coeffs[0], coeffs[1]
    steps.append(f"Коэффициенты: a = {a}, b = {b}")
    
    # Решаем: ax + b op 0
    # x op -b/a
    rhs = simplify(-b / a)
    
    # Если a < 0, меняем знак неравенства
    a_val = float(a.evalf())
    if a_val < 0:
        steps.append(f"a < 0, меняем знак неравенства")
        if op == '>':
            op = '<'
        elif op == '<':
            op = '>'
        elif op == '≥':
            op = '≤'
        elif op == '≤':
            op = '≥'
    
    # Форматируем RHS
    if rhs == int(rhs):
        rhs_str = str(int(rhs))
    else:
        rhs_str = f"{float(rhs.evalf()):.4f}".rstrip('0')
    
    steps.append(f"Решаем: x {op} {rhs_str}")
    
    # Определяем тип неравенства для sympy
    if op == '>':
        inequality = Ge(expanded, 0)
        solution = solve_univariate_inequality(expanded > 0, var, relational=False)
    elif op == '<':
        solution = solve_univariate_inequality(expanded < 0, var, relational=False)
    elif op == '≥':
        solution = solve_univariate_inequality(expanded >= 0, var, relational=False)
    elif op == '≤':
        solution = solve_univariate_inequality(expanded <= 0, var, relational=False)
    
    solution_str = format_interval(solution)
    steps.append(f"Ответ: x {op} {rhs_str}")
    
    return {
        'original': expr_str,
        'variable': variable,
        'solution': solution_str,
        'solution_interval': solution,
        'steps': steps,
        'explanation': f"Линейное неравенство: x {op} {rhs_str}",
        'type': 'линейное',
    }


def solve_quadratic_inequality(expr_str: str, variable: str = 'x'):
    """
    Решает квадратичное неравенство вида: ax² + bx + c > 0
    """
    steps = []
    var = symbols(variable)
    
    steps.append(f"Исходное неравенство: {expr_str}")
    
    # Парсим левую часть
    try:
        left = parse_expr_user(expr_str.split('>')[0].split('<')[0].split('≥')[0].split('≤')[0].strip())
    except ValueError as e:
        raise ValueError(str(e))
    
    # Определяем знак
    op = '>'
    if '<' in expr_str:
        op = '<'
    elif '≥' in expr_str or '>=' in expr_str:
        op = '≥'
    elif '≤' in expr_str or '<=' in expr_str:
        op = '≤'
    
    # Правая часть
    if '>' in expr_str:
        right_str = expr_str.split('>')[1].strip()
    elif '<' in expr_str:
        right_str = expr_str.split('<')[1].strip()
    elif '≥' in expr_str or '>=' in expr_str:
        right_str = expr_str.split('≥')[1].strip() if '≥' in expr_str else expr_str.split('>=')[1].strip()
    elif '≤' in expr_str or '<=' in expr_str:
        right_str = expr_str.split('≤')[1].strip() if '≤' in expr_str else expr_str.split('<=')[1].strip()
    else:
        right_str = '0'
    
    right = parse_expr_user(right_str)
    
    # Переносим всё влево
    expr = simplify(left - right)
    expanded = expand(expr)
    steps.append(f"Переносим всё влево: {expanded} {op} 0")
    
    # Коэффициенты
    poly = Poly(expanded, var)
    degree = poly.degree()
    coeffs = poly.all_coeffs()
    
    if degree != 2:
        raise ValueError("Это не квадратное неравенство")
    
    a, b, c = coeffs[0], coeffs[1], coeffs[2]
    steps.append(f"Коэффициенты: a = {a}, b = {b}, c = {c}")
    
    # Дискриминант
    D = b**2 - 4*a*c
    steps.append(f"Дискриминант: D = b² - 4ac = {D}")
    
    # Корни
    roots = []
    if D > 0:
        sqrt_D = sqrt(D)
        x1 = (-b - sqrt_D) / (2*a)
        x2 = (-b + sqrt_D) / (2*a)
        roots = [x1, x2]
        steps.append(f"Корни: x₁ = {x1}, x₂ = {x2}")
    elif D == 0:
        x = -b / (2*a)
        roots = [x]
        steps.append(f"Один корень: x = {x}")
    
    # Решаем неравенство
    if op == '>':
        solution = solve_univariate_inequality(expanded > 0, var, relational=False)
    elif op == '<':
        solution = solve_univariate_inequality(expanded < 0, var, relational=False)
    elif op == '≥':
        solution = solve_univariate_inequality(expanded >= 0, var, relational=False)
    elif op == '≤':
        solution = solve_univariate_inequality(expanded <= 0, var, relational=False)
    
    solution_str = format_interval(solution)
    steps.append(f"Ответ: {solution_str}")
    
    # Пояснение
    if D > 0:
        explanation = f"Квадратное неравенство: D = {D} > 0, парабола пересекает ось x в двух точках"
    elif D == 0:
        explanation = f"Квадратное неравенство: D = 0, парабола касается оси x"
    else:
        explanation = f"Квадратное неравенство: D = {D} < 0, парабола не пересекает ось x"
    
    return {
        'original': expr_str,
        'variable': variable,
        'solution': solution_str,
        'solution_interval': solution,
        'steps': steps,
        'explanation': explanation,
        'type': 'квадратное',
    }


def solve_inequality(expr_str: str, variable: str = 'x'):
    """
    Определяет тип неравенства и решает его.
    """
    # Сначала пробуем как квадратное
    try:
        left = parse_expr_user(expr_str.split('>')[0].split('<')[0].split('≥')[0].split('≤')[0].strip())
        poly = Poly(left, variable)
        degree = poly.degree()
        
        if degree == 2:
            return solve_quadratic_inequality(expr_str, variable)
        elif degree == 1:
            return solve_linear_inequality(expr_str, variable)
        else:
            raise ValueError("Неравенство степени выше 2 — пока не поддерживается")
    except ValueError:
        pass
    
    # Если не получилось, пробуем линейное
    try:
        return solve_linear_inequality(expr_str, variable)
    except Exception:
        pass
    
    raise ValueError("Не удалось распознать тип неравенства. Поддерживаются линейные и квадратные.")
