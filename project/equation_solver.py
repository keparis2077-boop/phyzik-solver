"""
Символьный решатель уравнений на основе sympy.
Принимает строковое уравнение, упрощает и решает его.
"""

from sympy import (
    symbols, Eq, solve, simplify, expand, factor, collect,
    sqrt, pi, E, I, nsimplify, Rational,
    sin, cos, tan, asin, acos, atan,
    log, exp, Abs,
    sympify, SympifyError,
    S, solve_linear, Poly, fraction,
    Mul, Add, Pow,
)
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application,
    convert_xor, function_exponentiation,
)

# Трансформации для парсинга пользовательского ввода
PARSING_TRANSFORMATIONS = (
    standard_transformations +
    (implicit_multiplication_application, convert_xor, function_exponentiation)
)


def parse_equation(equation_str: str):
    """
    Парсит строку уравнения, возвращает левую и правую части.
    Поддерживает: x^2, 2*x, sin(x), sqrt(x), и т.д.
    """
    # Нормализуем ввод
    eq = equation_str.strip()
    
    # Заменяем визуальные символы на программные
    eq = eq.replace('×', '*').replace('÷', '/').replace('−', '-').replace('π', 'pi')
    
    # Разделяем по '='
    if '=' not in eq:
        # Если нет '=', считаем что уравнение = 0
        left_expr = parse_user_input(eq)
        return left_expr, S.Zero
    
    parts = eq.split('=', 1)
    left_expr = parse_user_input(parts[0])
    right_expr = parse_user_input(parts[1])
    
    return left_expr, right_expr


def parse_user_input(expr_str: str):
    """
    Безопасно парсит математическое выражение пользователя.
    """
    s = expr_str.strip()
    
    # Заменяем ^ на ** для синтаксиса Python
    s = s.replace('^', '**')
    
    try:
        expr = parse_expr(
            s,
            local_dict={'pi': pi, 'e': E, 'sqrt': sqrt, 'abs': Abs},
            transformations=PARSING_TRANSFORMATIONS,
            evaluate=True,
        )
        return expr
    except (SympifyError, Exception):
        raise ValueError(f"Не удалось распознать выражение: '{expr_str}'")


def format_to_math(expr, variable='x'):
    """
    Преобразует sympy выражение в красивую математическую нотацию.
    Например: 2*x + 5 -> '2x + 5', x**2 -> 'x²'
    """
    s = str(expr)
    
    # Заменяем ** на ^ для отображения
    s = s.replace('**', '^')
    
    # Убираем * между числами и переменными
    import re
    s = re.sub(r'(\d)([a-zA-Z])', r'\1\2', s)  # 2*x -> 2x
    s = re.sub(r'([a-zA-Z])(\d)', r'\1\2', s)  # x*2 -> x2
    
    # Заменяем ^2, ^3 на верхние индексы
    s = s.replace('^2', '²')
    s = s.replace('^3', '³')
    s = s.replace('^4', '⁴')
    s = s.replace('^5', '⁵')
    s = s.replace('^6', '⁶')
    s = s.replace('^7', '⁷')
    s = s.replace('^8', '⁸')
    s = s.replace('^9', '⁹')
    
    # Заменяем sqrt на √
    s = s.replace('sqrt', '√')
    
    # Заменяем pi на π
    s = s.replace('pi', 'π')
    
    # Заменяем e на число Эйлера
    s = s.replace('E', 'e')
    
    # Заменяем I на i (мнимая единица)
    s = s.replace('I', 'i')
    
    # Заменяем умножение и деление
    s = s.replace(' / ', ' ÷ ')
    
    # Убираем лишние скобки
    s = re.sub(r'\(([^()]+)\)', r'\1', s)
    
    return s


def format_equation_to_standard(expr, variable='x'):
    """
    Форматирует уравнение в стандартный вид с красивыми коэффициентами.
    Например: 2*x + 5 - 15 -> '2x - 10 = 0'
    """
    import re
    
    # Создаём символ переменной
    var = symbols(variable)
    
    # Получаем коэффициенты
    poly = Poly(expr, var)
    degree = poly.degree()
    coeffs = poly.all_coeffs()
    
    if degree == 0:
        return f"{coeffs[0]} = 0"
    
    parts = []
    for i, coeff in enumerate(coeffs):
        power = degree - i
        
        # Пропускаем нулевые коэффициенты (кроме свободного члена)
        coeff_val = float(coeff.evalf()) if hasattr(coeff, 'evalf') else float(coeff)
        if coeff_val == 0 and power > 0:
            continue
        
        # Форматируем коэффициент
        coeff_str = format_coefficient(coeff, variable)
        
        # Форматируем степень
        if power == 0:
            term = coeff_str
        elif power == 1:
            term = f"{coeff_str}{variable}"
        else:
            term = f"{coeff_str}{variable}²" if power == 2 else f"{coeff_str}{variable}^{power}"
        
        parts.append(term)
    
    # Собираем уравнение с правильными пробелами
    equation_parts = []
    for i, part in enumerate(parts):
        if i == 0:
            equation_parts.append(part)
        else:
            if part.startswith('-'):
                equation_parts.append(' - ' + part[1:].strip())
            else:
                equation_parts.append(' + ' + part)
    
    equation = ''.join(equation_parts) + ' = 0'
    
    return equation


def format_coefficient(coeff, variable):
    """
    Форматирует коэффициент красиво.
    """
    coeff_val = float(coeff.evalf()) if hasattr(coeff, 'evalf') else float(coeff)
    
    if coeff_val == 1:
        return ''
    elif coeff_val == -1:
        return '-'
    elif coeff_val == int(coeff_val):
        return str(int(coeff_val))
    else:
        return f"{coeff_val:.2f}".rstrip('0').rstrip('.')


def simplify_expression(expr):
    """Упрощает выражение."""
    try:
        simplified = simplify(expr)
        return simplified
    except Exception:
        return expand(expr)


def solve_equation(equation_str: str, variable: str = None):
    """
    Главное решение уравнения.
    
    Args:
        equation_str: строка уравнения, например "2*x + 5 = 15" или "x^2 - 5*x + 6 = 0"
        variable: переменная для решения (по умолчанию 'x')
    
    Returns:
        dict с ключами:
            - original: исходное уравнение (строка)
            - simplified: упрощённое уравнение (строка)
            - variable: переменная решения
            - solutions: список решений
            - steps: список шагов решения
            - explanation: текстовое пояснение
            - type: тип уравнения (linear, quadratic, etc.)
    """
    if variable is None:
        variable = 'x'
    
    steps = []
    var = symbols(variable)
    
    # Шаг 1: Парсим уравнение
    try:
        left, right = parse_equation(equation_str)
    except ValueError as e:
        raise ValueError(str(e))
    
    steps.append(f"Исходное уравнение: {equation_str}")
    
    # Шаг 2: Переносим всё в левую часть: left - right = 0
    equation = Eq(left, right)
    steps.append(f"Записываем: {left} = {right}")
    
    # Переносим в стандартную форму
    expr = simplify(left - right)
    expanded = expand(expr)
    steps.append(f"Переносим всё влево: {expanded} = 0")
    
    # Шаг 3: Упрощаем
    simplified = simplify(expanded)
    steps.append(f"Упрощаем: {simplified} = 0")
    
    # Шаг 4: Определяем тип уравнения
    poly = Poly(simplified, var)
    degree = poly.degree()
    coeffs = poly.all_coeffs()
    
    type_name = "уравнение"
    if degree == 0:
        # Константа
        if simplified == 0:
            return {
                'original': equation_str,
                'simplified': '0 = 0',
                'variable': variable,
                'solutions': ['любое число'],
                'steps': steps + ["Уравнение верно для любого x"],
                'explanation': 'Тождество: уравнение верно для любого x',
                'type': 'identity',
            }
        else:
            return {
                'original': equation_str,
                'simplified': str(simplified),
                'variable': variable,
                'solutions': ['нет решений'],
                'steps': steps + [f"Константа ≠ 0: решений нет"],
                'explanation': 'Уравнение не имеет решений (противоречие)',
                'type': 'contradiction',
            }
    elif degree == 1:
        type_name = "линейное"
    elif degree == 2:
        type_name = "квадратное"
    elif degree == 3:
        type_name = "кубическое"
    elif degree > 3:
        type_name = f"полиномиальное степени {degree}"
    
    steps.append(f"Тип уравнения: {type_name}")
    
    # Шаг 5: Показываем коэффициенты для линейных и квадратных
    if degree == 1:
        # ax + b = 0
        a, b = coeffs[0], coeffs[1]
        steps.append(f"Коэффициенты: a = {a}, b = {b}")
        steps.append(f"Решаем: {a}*{variable} + ({b}) = 0")
    elif degree == 2:
        # ax² + bx + c = 0
        a, b, c = coeffs[0], coeffs[1], coeffs[2]
        steps.append(f"Коэффициенты: a = {a}, b = {b}, c = {c}")
        # Дискриминант
        D = b**2 - 4*a*c
        D_float = float(D.evalf()) if hasattr(D, 'evalf') else D
        steps.append(f"Дискриминант: D = b² - 4ac = {b}² - 4·{a}·{c} = {D}")
        
        if D_float > 0:
            steps.append("D > 0: два корня")
        elif D_float == 0:
            steps.append("D = 0: один корень")
        else:
            steps.append(f"D = {D} < 0: действительных корней нет")
    
    # Шаг 6: Решаем (только действительные корни)
    try:
        raw_solutions = solve(Eq(left, right), var, rational=True)
    except Exception:
        try:
            raw_solutions = solve(simplified, var)
        except Exception:
            raise ValueError("Не удалось решить уравнение")
    
    # Фильтруем только действительные корни
    real_solutions = [sol for sol in raw_solutions if sol.is_real is not False]
    has_complex = len(real_solutions) < len(raw_solutions)
    
    # Форматируем решения
    solutions = []
    solution_details = []
    
    if not real_solutions:
        solutions = ['нет решений']
    else:
        for i, sol in enumerate(real_solutions):
            try:
                numeric = float(sol.evalf())
            except (TypeError, ValueError):
                numeric = None
            
            # Красивое представление
            if sol == int(sol):
                nice_exact = str(int(sol))
            elif numeric is not None and abs(sol - numeric) < 1e-10:
                nice_exact = f"{numeric:.4f}".rstrip('0')
            else:
                nice_exact = str(sol)
            
            if len(real_solutions) == 1:
                var_suffix = ""
            else:
                var_suffix = f"_{i+1}"
            
            solution_text = f"{variable}{var_suffix} = {nice_exact}"
            solutions.append(solution_text)
            solution_details.append({
                'exact': sol,
                'numeric': numeric,
                'text': solution_text,
            })
    
    # Шаг 7: Формируем пояснение
    if degree == 1:
        a, b = coeffs[0], coeffs[1]
        if a != 0:
            steps.append(f"{variable} = -({b}) / ({a}) = {solutions[0].split('=')[1].strip()}")
        explanation = f"Линейное уравнение: {variable} = -b/a"
    
    elif degree == 2:
        a, b, c = coeffs[0], coeffs[1], coeffs[2]
        D = b**2 - 4*a*c
        if has_complex:
            steps.append("D < 0: действительных корней нет (комплексные корни)")
            explanation = f"Квадратное уравнение: D = {D} < 0, корни комплексные"
        elif D > 0:
            sqrt_D = sqrt(D)
            steps.append(f"x₁ = (-b + √D) / 2a = ({-b} + √{D}) / ({2*a}) = {solutions[0].split('=')[1].strip()}")
            steps.append(f"x₂ = (-b - √D) / 2a = ({-b} - √{D}) / ({2*a}) = {solutions[1].split('=')[1].strip()}")
            explanation = f"Квадратное уравнение: D = {D} > 0, два корня"
        elif D == 0:
            x = -b / (2*a)
            steps.append(f"x = -b / (2a) = {-b} / ({2*a}) = {solutions[0].split('=')[1].strip()}")
            explanation = f"Квадратное уравнение: D = 0, один корень"
        else:
            explanation = f"Квадратное уравнение: D = {D} < 0, действительных корней нет"
    
    else:
        for i, sol in enumerate(solution_details):
            steps.append(f"{variable}_{i+1} = {sol['text'].split('=')[1].strip()}")
        explanation = f"Полиномиальное уравнение степени {degree}: решено численно"
    
    steps.append(f"Ответ: {'; '.join(solutions)}")
    
    # Формируем полное представление уравнения
    full_equation = format_equation_to_standard(simplified, variable)
    
    # Красивое представление исходного уравнения
    original_formatted = format_to_math(left, variable) + ' = ' + format_to_math(right, variable)
    
    return {
        'original': equation_str,
        'original_formatted': original_formatted,
        'simplified': str(simplified),
        'simplified_formatted': format_to_math(simplified, variable),
        'full_equation': full_equation,
        'variable': variable,
        'solutions': solutions,
        'solution_details': solution_details,
        'steps': steps,
        'explanation': explanation,
        'type': type_name,
        'degree': degree,
        'coefficients': [str(c) for c in coeffs],
    }


def solve_system_of_equations(equations: list, variables: list = None):
    """
    Решает систему уравнений.
    
    Args:
        equations: список строк уравнений
        variables: список переменных
    
    Returns:
        dict с решениями и шагами
    """
    if variables is None:
        variables = ['x', 'y']
    
    steps = []
    syms = [symbols(v) for v in variables]
    
    steps.append(f"Система уравнений с переменными: {', '.join(variables)}")
    
    # Парсим уравнения
    eqs = []
    for eq_str in equations:
        try:
            left, right = parse_equation(eq_str)
            eqs.append(Eq(left, right))
            steps.append(f"Уравнение: {eq_str}")
        except ValueError as e:
            raise ValueError(str(e))
    
    # Решаем
    try:
        solution = solve(eqs, syms)
    except Exception as e:
        raise ValueError(f"Не удалось решить систему: {str(e)}")
    
    if not solution:
        return {
            'solutions': ['нет решений'],
            'steps': steps + ['Система не имеет решений'],
            'explanation': 'Система уравнений не имеет решений',
        }
    
    # Форматируем результаты
    steps.append("Решаем систему...")
    
    if isinstance(solution, dict):
        result_parts = []
        for sym, val in solution.items():
            val_str = str(val)
            if val == int(val):
                val_str = str(int(val))
            result_parts.append(f"{sym} = {val_str}")
            steps.append(f"{sym} = {val_str}")
        
        return {
            'solutions': result_parts,
            'steps': steps,
            'explanation': 'Система уравнений решена методом подстановки',
            'solution_dict': solution,
        }
    elif isinstance(solution, (list, tuple)):
        result_parts = []
        for i, val in enumerate(solution):
            val_str = str(val)
            if val == int(val):
                val_str = str(int(val))
            result_parts.append(f"{variables[i]} = {val_str}")
            steps.append(f"{variables[i]} = {val_str}")
        
        return {
            'solutions': result_parts,
            'steps': steps,
            'explanation': 'Система уравнений решена методом исключения',
            'solution_list': solution,
        }
    
    return {
        'solutions': [str(solution)],
        'steps': steps,
        'explanation': 'Решение найдено',
    }


def simplify_expression_only(expr_str: str):
    """
    Просто упрощает выражение без уравнения. Поддерживает дроби.
    """
    try:
        expr = parse_user_input(expr_str)
        simplified = simplify(expr)
        expanded = expand(expr)
        
        # Проверяем, является ли результат дробью
        numerator, denominator = fraction(simplified)
        
        # Упрощаем числитель и знаменатель
        num_simplified = simplify(numerator)
        den_simplified = simplify(denominator)
        
        # Проверяем, является ли результат простой дробью (число/число)
        is_simple_fraction = False
        frac_numerator = None
        frac_denominator = None
        frac_decimal = None
        
        try:
            if num_simplified.is_number and den_simplified.is_number and den_simplified != 1:
                # Получаем численные значения
                num_val = float(num_simplified.evalf())
                den_val = float(den_simplified.evalf())
                
                if den_val != 0 and den_val != 1:
                    # Пытаемся представить как Rational
                    rat = Rational(num_val, den_val).limit_denominator()
                    frac_numerator = int(rat.numerator)
                    frac_denominator = int(rat.denominator)
                    frac_decimal = float(rat)
                    is_simple_fraction = True
        except (TypeError, ValueError, AttributeError):
            pass
        
        # Формируем шаги
        steps = [
            f"Исходное выражение: {expr_str}",
        ]
        
        if is_simple_fraction:
            steps.append(f"Упрощённое: {num_simplified} / {den_simplified}")
            steps.append(f"Как дробь: {frac_numerator} / {frac_denominator}")
            steps.append(f"Как десятичная: {frac_decimal:.4f}".rstrip('0'))
        else:
            steps.append(f"Упрощённое: {simplified}")
            steps.append(f"Раскрытое: {expanded}")
        
        result = {
            'original': expr_str,
            'simplified': str(simplified),
            'expanded': str(expanded),
            'is_fraction': is_simple_fraction,
            'numerator': frac_numerator,
            'denominator': frac_denominator,
            'decimal': f"{frac_decimal:.4f}".rstrip('0') if frac_decimal is not None else None,
        }
        
        # Если есть дробь в выражении, показываем пошаговое упрощение
        if '/' in expr_str or '÷' in expr_str or '1/' in expr_str:
            steps.insert(1, "Обнаружена дробь — упрощаем числитель и знаменатель отдельно")
        
        result['steps'] = steps
        return result
        
    except ValueError as e:
        raise ValueError(str(e))
