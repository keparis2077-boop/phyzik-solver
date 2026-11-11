"""
Математические задачи: алгебра, геометрия, тригонометрия
"""

MATH_TASKS = {
    # ===== АЛГЕБРА =====
    'quadratic_equation': {
        'id': 'quadratic_equation',
        'name': 'Квадратное уравнение',
        'icon': '📊',
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
    
    'linear_equation': {
        'id': 'linear_equation',
        'name': 'Линейное уравнение',
        'icon': '📈',
        'category': 'Алгебра',
        'difficulty': '7',
        'condition': 'Решите линейное уравнение ax + b = 0',
        'formulas': ['x = -b / a'],
        'inputs': {
            'a': {'label': 'a', 'placeholder': 'Например: 2'},
            'b': {'label': 'b', 'placeholder': 'Например: -10'},
        },
        'solve': lambda data: solve_linear(data),
    },
    
    'system_equations': {
        'id': 'system_equations',
        'name': 'Система уравнений',
        'icon': '📋',
        'category': 'Алгебра',
        'difficulty': '9',
        'condition': 'Решите систему уравнений:\na₁x + b₁y = c₁\na₂x + b₂y = c₂',
        'formulas': ['D = a₁b₂ - a₂b₁', 'x = (c₁b₂ - c₂b₁) / D', 'y = (a₁c₂ - a₂c₁) / D'],
        'inputs': {
            'a1': {'label': 'a₁', 'placeholder': 'Коэффициент при x в 1-м уравнении'},
            'b1': {'label': 'b₁', 'placeholder': 'Коэффициент при y в 1-м уравнении'},
            'c1': {'label': 'c₁', 'placeholder': 'Свободный член 1-го уравнения'},
            'a2': {'label': 'a₂', 'placeholder': 'Коэффициент при x во 2-м уравнении'},
            'b2': {'label': 'b₂', 'placeholder': 'Коэффициент при y во 2-м уравнении'},
            'c2': {'label': 'c₂', 'placeholder': 'Свободный член 2-го уравнения'},
        },
        'solve': lambda data: solve_system(data),
    },
    
    # ===== ГЕОМЕТРИЯ =====
    'triangle_area': {
        'id': 'triangle_area',
        'name': 'Площадь треугольника',
        'icon': '🔺',
        'category': 'Геометрия',
        'difficulty': '7-8',
        'condition': 'Найдите площадь, основание или высоту треугольника',
        'formulas': ['S = ½ · a · h'],
        'inputs': {
            'a': {'label': 'Основание a', 'placeholder': 'Например: 10'},
            'h': {'label': 'Высота h', 'placeholder': 'Например: 5'},
            'S': {'label': 'Площадь S', 'placeholder': 'Например: 20'},
        },
        'unknowns': ['a', 'h', 'S'],
        'solve': lambda data: solve_triangle_area(data),
    },
    
    'circle_area': {
        'id': 'circle_area',
        'name': 'Площадь круга',
        'icon': '⭕',
        'category': 'Геометрия',
        'difficulty': '7',
        'condition': 'Найдите площадь круга или радиус',
        'formulas': ['S = π · r²'],
        'inputs': {
            'r': {'label': 'Радиус r', 'placeholder': 'Например: 5'},
            'S': {'label': 'Площадь S', 'placeholder': 'Например: 78.5'},
        },
        'unknowns': ['r', 'S'],
        'solve': lambda data: solve_circle_area(data),
    },
    
    'pythagorean_theorem': {
        'id': 'pythagorean_theorem',
        'name': 'Теорема Пифагора',
        'icon': '📐',
        'category': 'Геометрия',
        'difficulty': '8',
        'condition': 'Найдите гипотенузу или катет прямоугольного треугольника',
        'formulas': ['c² = a² + b²', 'a = √(c² - b²)', 'b = √(c² - a²)'],
        'inputs': {
            'a': {'label': 'Катет a', 'placeholder': 'Введите значение'},
            'b': {'label': 'Катет b', 'placeholder': 'Введите значение'},
            'c': {'label': 'Гипотенуза c', 'placeholder': 'Введите значение'},
        },
        'unknowns': ['a', 'b', 'c'],
        'solve': lambda data: solve_pythagorean(data),
    },
    
    # ===== ТРИГОНОМЕТРИЯ =====
    'sin_cos_tan': {
        'id': 'sin_cos_tan',
        'name': 'Тригонометрические функции',
        'icon': '📈',
        'category': 'Тригонометрия',
        'difficulty': '9-10',
        'condition': 'Найдите sin, cos, tan или угол',
        'formulas': ['sin(α) = противолежащий катет / гипотенуза', 'cos(α) = прилежащий катет / гипотенуза', 'tan(α) = sin(α) / cos(α)'],
        'inputs': {
            'angle': {'label': 'Угол α (градусы)', 'placeholder': 'Например: 30'},
            'sin': {'label': 'sin(α)', 'placeholder': 'Например: 0.5'},
            'cos': {'label': 'cos(α)', 'placeholder': 'Например: 0.866'},
            'tan': {'label': 'tan(α)', 'placeholder': 'Например: 0.577'},
        },
        'unknowns': ['angle', 'sin', 'cos', 'tan'],
        'solve': lambda data: solve_trig_functions(data),
    },
    
    'law_of_cosines': {
        'id': 'law_of_cosines',
        'name': 'Теорема косинусов',
        'icon': '📏',
        'category': 'Тригонометрия',
        'difficulty': '9-10',
        'condition': 'Найдите сторону или угол треугольника',
        'formulas': ['c² = a² + b² - 2ab·cos(γ)'],
        'inputs': {
            'a': {'label': 'Сторона a', 'placeholder': 'Например: 5'},
            'b': {'label': 'Сторона b', 'placeholder': 'Например: 7'},
            'gamma': {'label': 'Угол γ (градусы)', 'placeholder': 'Например: 60'},
            'c': {'label': 'Сторона c', 'placeholder': 'Например: 8'},
        },
        'unknowns': ['a', 'b', 'gamma', 'c'],
        'solve': lambda data: solve_law_of_cosines(data),
    },
    
    # ===== ПРОЧИЕ =====
    'right_triangle': {
        'id': 'right_triangle',
        'name': 'Прямоугольный треугольник',
        'icon': '📐',
        'category': 'Геометрия',
        'difficulty': '8-9',
        'condition': 'Найдите неизвестную сторону или угол прямоугольного треугольника по известным элементам',
        'formulas': [
            'c² = a² + b² (теорема Пифагора)',
            'sin(α) = a / c',
            'cos(α) = b / c',
            'tan(α) = a / b',
            'α + β = 90°',
        ],
        'inputs': {
            'a': {'label': 'Катет a', 'placeholder': 'Введите значение'},
            'b': {'label': 'Катет b', 'placeholder': 'Введите значение'},
            'c': {'label': 'Гипотенуза c', 'placeholder': 'Введите значение'},
            'alpha': {'label': 'Угол α (градусы)', 'placeholder': 'Например: 30'},
        },
        'unknowns': ['a', 'b', 'c', 'alpha'],
        'solve': lambda data: solve_right_triangle(data),
    },

    # ===== АНАЛИЗ =====
    'derivative_power': {
        'id': 'derivative_power',
        'name': 'Производная степени',
        'icon': '📉',
        'category': 'Анализ',
        'difficulty': '10-11',
        'condition': 'Найдите производную функции f(x) = xⁿ в точке x',
        'formulas': ["f'(x) = n · xⁿ⁻¹"],
        'inputs': {
            'n': {'label': 'n (степень)', 'placeholder': 'Например: 3'},
            'x': {'label': 'x (точка вычисления)', 'placeholder': 'Например: 2'},
        },
        'solve': lambda data: solve_derivative_power(data),
    },

    'integral_power': {
        'id': 'integral_power',
        'name': 'Интеграл степени',
        'icon': '📊',
        'category': 'Анализ',
        'difficulty': '11',
        'condition': 'Вычислите определённый интеграл ∫(xⁿ) dx от a до b',
        'formulas': ['∫xⁿ dx = xⁿ⁺¹/(n+1)'],
        'inputs': {
            'n': {'label': 'n (степень)', 'placeholder': 'Например: 2'},
            'a': {'label': 'a (нижний предел)', 'placeholder': 'Например: 0'},
            'b': {'label': 'b (верхний предел)', 'placeholder': 'Например: 3'},
        },
        'solve': lambda data: solve_integral_power(data),
    },

    'limit_function': {
        'id': 'limit_function',
        'name': 'Предел функции',
        'icon': '🔍',
        'category': 'Анализ',
        'difficulty': '10-11',
        'condition': 'Вычислите предел замечательной функции',
        'formulas': ['lim(x→0) sin(x)/x = 1', 'lim(x→∞) (1+1/x)ˣ = e'],
        'inputs': {
            'type': {'label': 'Тип предела', 'placeholder': 'sin (sin(x)/x) или euler ((1+1/x)^x)', 'input_type': 'text'},
        },
        'solve': lambda data: solve_limit(data),
    },

    # ===== ВЕКТОРЫ =====
    'vector_addition': {
        'id': 'vector_addition',
        'name': 'Сложение векторов',
        'icon': '➡️',
        'category': 'Векторы',
        'difficulty': '9-10',
        'condition': 'Найдите модуль суммы двух векторов и угол между суммой и первым вектором',
        'formulas': ['|a + b| = √(a² + b² + 2ab·cos(γ))', 'α = arctan(b·sin(γ) / (a + b·cos(γ)))'],
        'inputs': {
            'a': {'label': 'Модуль вектора a', 'placeholder': 'Например: 5'},
            'b': {'label': 'Модуль вектора b', 'placeholder': 'Например: 3'},
            'angle': {'label': 'Угол γ между векторами (градусы)', 'placeholder': 'Например: 60'},
        },
        'solve': lambda data: solve_vector_addition(data),
    },

    'vector_scalar_product': {
        'id': 'vector_scalar_product',
        'name': 'Скалярное произведение',
        'icon': '🔢',
        'category': 'Векторы',
        'difficulty': '10',
        'condition': 'Вычислите скалярное произведение двух векторов',
        'formulas': ['a · b = |a| · |b| · cos(γ)'],
        'inputs': {
            'a': {'label': 'Модуль вектора a', 'placeholder': 'Например: 4'},
            'b': {'label': 'Модуль вектора b', 'placeholder': 'Например: 6'},
            'angle': {'label': 'Угол γ (градусы)', 'placeholder': 'Например: 45'},
        },
        'solve': lambda data: solve_scalar_product(data),
    },

    'vector_projection': {
        'id': 'vector_projection',
        'name': 'Проекция вектора',
        'icon': '📐',
        'category': 'Векторы',
        'difficulty': '10',
        'condition': 'Найдите проекцию вектора a на направление вектора b',
        'formulas': ['Pr_b(a) = |a| · cos(γ)'],
        'inputs': {
            'a': {'label': 'Модуль вектора a', 'placeholder': 'Например: 10'},
            'angle': {'label': 'Угол γ между векторами (градусы)', 'placeholder': 'Например: 30'},
        },
        'solve': lambda data: solve_projection(data),
    },

    # ===== ТЕОРИЯ ВЕРОЯТНОСТЕЙ =====
    'probability_classic': {
        'id': 'probability_classic',
        'name': 'Классическая вероятность',
        'icon': '🎲',
        'category': 'Теория вероятностей',
        'difficulty': '9-10',
        'condition': 'Вычислите вероятность по формуле P = m/n',
        'formulas': ['P = m / n', 'm — благоприятные исходы', 'n — все исходы'],
        'inputs': {
            'm': {'label': 'm (благоприятные исходы)', 'placeholder': 'Например: 3'},
            'n': {'label': 'n (все исходы)', 'placeholder': 'Например: 6'},
        },
        'solve': lambda data: solve_probability_classic(data),
    },

    'probability_combinatorics': {
        'id': 'probability_combinatorics',
        'name': 'Комбинаторика',
        'icon': '🔢',
        'category': 'Теория вероятностей',
        'difficulty': '10-11',
        'condition': 'Найдите число перестановок/размещений/сочетаний',
        'formulas': ['P(n) = n!', 'A(n,k) = n!/(n-k)!', 'C(n,k) = n!/(k!(n-k)!)'],
        'inputs': {
            'n': {'label': 'n (элементов)', 'placeholder': 'Например: 5'},
            'k': {'label': 'k (выбираем)', 'placeholder': 'Например: 3'},
            'method': {'label': 'Метод (permutation/arrangement/combination)', 'placeholder': 'combination', 'input_type': 'text'},
        },
        'solve': lambda data: solve_combinatorics(data),
    },

    'probability_distribution': {
        'id': 'probability_distribution',
        'name': 'Распределение Бернулли',
        'icon': '📊',
        'category': 'Теория вероятностей',
        'difficulty': '11',
        'condition': 'Вычислите вероятность по формуле Бернулли (biномное распределение)',
        'formulas': ['P(k,n) = C(n,k) · pᵏ · (1-p)ⁿ⁻ᵏ'],
        'inputs': {
            'n': {'label': 'n (испытаний)', 'placeholder': 'Например: 10'},
            'k': {'label': 'k (успехов)', 'placeholder': 'Например: 3'},
            'p': {'label': 'p (вероятность успеха)', 'placeholder': 'Например: 0.5'},
        },
        'solve': lambda data: solve_probability_distribution(data),
    },
}


def solve_quadratic(data):
    """Решение квадратного уравнения"""
    def to_float(key):
        val = data.get(key, '0')
        if not val or val.strip() == '':
            return 0.0
        return float(val)
    
    a = to_float('a')
    b = to_float('b')
    c = to_float('c')
    
    if a == 0:
        raise ValueError("a не может быть 0 для квадратного уравнения")
    
    D = b**2 - 4*a*c
    steps = [
        f"Дано: a={a}, b={b}, c={c}",
        f"Дискриминант: D = b² - 4ac = {b}² - 4·{a}·{c} = {D}",
    ]
    
    if D < 0:
        steps.append("D < 0: корней нет")
        return {}, steps, "Квадратное уравнение не имеет действительных корней"
    
    elif D == 0:
        x = -b / (2*a)
        steps.append(f"D = 0: один корень x = -b/(2a) = {x:.2f}")
        return {'x': f'{x:.2f}'}, steps, "Квадратное уравнение имеет один корень"
    
    else:
        x1 = (-b + D**0.5) / (2*a)
        x2 = (-b - D**0.5) / (2*a)
        steps.append(f"D > 0: два корня")
        steps.append(f"x₁ = (-b + √D) / 2a = {x1:.2f}")
        steps.append(f"x₂ = (-b - √D) / 2a = {x2:.2f}")
        return {'x₁': f'{x1:.2f}', 'x₂': f'{x2:.2f}'}, steps, "Квадратное уравнение имеет два корня"


def solve_linear(data):
    """Решение линейного уравнения"""
    def to_float(key):
        val = data.get(key, '0')
        if not val or val.strip() == '':
            return 0.0
        return float(val)
    
    a = to_float('a')
    b = to_float('b')
    
    if a == 0:
        if b == 0:
            return {'x': 'любое'}, ["a=0, b=0: любое x — решение"], "Уравнение имеет бесконечно много решений"
        else:
            raise ValueError("Уравнение не имеет решений")
    
    x = -b / a
    steps = [
        f"Дано: a={a}, b={b}",
        f"x = -b/a = -{b}/{a} = {x:.2f}",
    ]
    return {'x': f'{x:.2f}'}, steps, "Линейное уравнение имеет один корень"


def solve_system(data):
    """Решение системы уравнений"""
    def to_float(key):
        val = data.get(key, '0')
        if not val or val.strip() == '':
            return 0.0
        return float(val)
    
    a1, b1, c1 = to_float('a1'), to_float('b1'), to_float('c1')
    a2, b2, c2 = to_float('a2'), to_float('b2'), to_float('c2')
    
    D = a1*b2 - a2*b1
    
    if D == 0:
        raise ValueError("Система не имеет единственного решения (определитель равен 0)")
    
    x = (c1*b2 - c2*b1) / D
    y = (a1*c2 - a2*c1) / D
    
    steps = [
        f"Определитель: D = a₁b₂ - a₂b₁ = {a1}·{b2} - {a2}·{b1} = {D}",
        f"x = (c₁b₂ - c₂b₁) / D = ({c1}·{b2} - {c2}·{b1}) / {D} = {x:.2f}",
        f"y = (a₁c₂ - a₂c₁) / D = ({a1}·{c2} - {a2}·{c1}) / {D} = {y:.2f}",
    ]
    return {'x': f'{x:.2f}', 'y': f'{y:.2f}'}, steps, "Система уравнений имеет единственное решение"


def solve_triangle_area(data):
    """Площадь треугольника"""
    unknown = data.get('unknown', '').strip()
    a = data.get('a', '').strip()
    h = data.get('h', '').strip()
    S = data.get('S', '').strip()
    
    # Fallback для задач без выбора unknown
    if not unknown:
        filled = [k for k, v in [('a', a), ('h', h), ('S', S)] if v]
        if len(filled) == 2:
            missing = ['a', 'h', 'S']
            for m in missing:
                if m not in filled:
                    unknown = m
                    break
        else:
            unknown = 'S'
    
    if not unknown:
        raise ValueError("Выберите, что нужно найти!")
    
    a_val = float(a) if a else None
    h_val = float(h) if h else None
    S_val = float(S) if S else None
    
    if unknown == 'S':
        if a_val is None or h_val is None:
            raise ValueError("Для нахождения площади нужны основание и высота")
        S_val = 0.5 * a_val * h_val
        steps = [
            f"Дано: a={a_val}, h={h_val}",
            f"S = ½ · a · h = 0.5 · {a_val} · {h_val} = {S_val:.2f}",
        ]
        return {'S': f'{S_val:.2f}'}, steps, "Площадь треугольника вычисляется по формуле S = ½ah"
    
    elif unknown == 'a':
        if S_val is None or h_val is None:
            raise ValueError("Для нахождения основания нужны площадь и высота")
        if h_val == 0:
            raise ValueError("Высота не может быть равна 0")
        a_val = 2 * S_val / h_val
        steps = [
            f"Дано: S={S_val}, h={h_val}",
            f"a = 2S / h = 2·{S_val} / {h_val} = {a_val:.2f}",
        ]
        return {'a': f'{a_val:.2f}'}, steps, "Площадь треугольника: S = ½ah, откуда a = 2S/h"
    
    elif unknown == 'h':
        if S_val is None or a_val is None:
            raise ValueError("Для нахождения высоты нужны площадь и основание")
        if a_val == 0:
            raise ValueError("Основание не может быть равно 0")
        h_val = 2 * S_val / a_val
        steps = [
            f"Дано: S={S_val}, a={a_val}",
            f"h = 2S / a = 2·{S_val} / {a_val} = {h_val:.2f}",
        ]
        return {'h': f'{h_val:.2f}'}, steps, "Площадь треугольника: S = ½ah, откуда h = 2S/a"


def solve_circle_area(data):
    """Площадь круга"""
    import math
    unknown = data.get('unknown', '').strip()
    r = data.get('r', '').strip()
    S = data.get('S', '').strip()
    
    # Fallback для задач без выбора unknown
    if not unknown:
        if r:
            unknown = 'S'
        elif S:
            unknown = 'r'
        else:
            raise ValueError("Введите радиус или площадь")
    
    r_val = float(r) if r else None
    S_val = float(S) if S else None
    
    r_val = float(r) if r else None
    S_val = float(S) if S else None
    
    if unknown == 'S':
        if r_val is None:
            raise ValueError("Для нахождения площади нужен радиус")
        S_val = math.pi * r_val**2
        steps = [
            f"Дано: r={r_val}",
            f"S = π · r² = 3.14159 · {r_val}² = {S_val:.2f}",
        ]
        return {'S': f'{S_val:.2f}'}, steps, "Площадь круга вычисляется по формуле S = πr²"
    
    elif unknown == 'r':
        if S_val is None:
            raise ValueError("Для нахождения радиуса нужна площадь")
        if S_val <= 0:
            raise ValueError("Площадь должна быть положительной")
        r_val = (S_val / math.pi)**0.5
        steps = [
            f"Дано: S={S_val}",
            f"r = √(S/π) = √({S_val}/3.14159) = {r_val:.2f}",
        ]
        return {'r': f'{r_val:.2f}'}, steps, "Площадь круга: S = πr², откуда r = √(S/π)"


def solve_pythagorean(data):
    """Теорема Пифагора"""
    unknown = data.get('unknown', '').strip()
    a = data.get('a', '').strip()
    b = data.get('b', '').strip()
    c = data.get('c', '').strip()
    
    # Fallback для задач без выбора unknown
    if not unknown:
        filled = [k for k, v in [('a', a), ('b', b), ('c', c)] if v]
        if len(filled) == 2:
            missing = ['a', 'b', 'c']
            for m in missing:
                if m not in filled:
                    unknown = m
                    break
        else:
            unknown = 'c'
    
    if not unknown:
        raise ValueError("Выберите, что нужно найти!")
    
    # Преобразуем заполненные поля в числа
    a_val = float(a) if a else None
    b_val = float(b) if b else None
    c_val = float(c) if c else None
    
    if unknown == 'a':
        # Ищем a
        if c_val <= b_val:
            raise ValueError("Гипотенуза должна быть больше катета")
        a_val = (c_val**2 - b_val**2)**0.5
        steps = [
            f"Дано: b={b_val}, c={c_val}",
            f"a = √(c² - b²) = √({c_val}² - {b_val}²) = √({c_val**2 - b_val**2}) = {a_val:.2f}",
        ]
        return {'a': f'{a_val:.2f}'}, steps, "Теорема Пифагора: c² = a² + b²"
    
    elif unknown == 'b':
        # Ищем b
        if c_val <= a_val:
            raise ValueError("Гипотенуза должна быть больше катета")
        b_val = (c_val**2 - a_val**2)**0.5
        steps = [
            f"Дано: a={a_val}, c={c_val}",
            f"b = √(c² - a²) = √({c_val}² - {a_val}²) = √({c_val**2 - a_val**2}) = {b_val:.2f}",
        ]
        return {'b': f'{b_val:.2f}'}, steps, "Теорема Пифагора: c² = a² + b²"
    
    elif unknown == 'c':
        # Ищем c
        c_val = (a_val**2 + b_val**2)**0.5
        steps = [
            f"Дано: a={a_val}, b={b_val}",
            f"c = √(a² + b²) = √({a_val}² + {b_val}²) = √({a_val**2 + b_val**2}) = {c_val:.2f}",
        ]
        return {'c': f'{c_val:.2f}'}, steps, "Теорема Пифагора: c² = a² + b²"


def solve_trig_functions(data):
    """Тригонометрические функции"""
    import math
    unknown = data.get('unknown', '').strip()
    angle = data.get('angle', '').strip()
    sin_val = data.get('sin', '').strip()
    cos_val = data.get('cos', '').strip()
    tan_val = data.get('tan', '').strip()
    
    # Fallback для задач без выбора unknown
    if not unknown:
        if angle:
            unknown = 'sin'
        elif sin_val:
            unknown = 'angle'
        elif cos_val:
            unknown = 'angle'
        elif tan_val:
            unknown = 'angle'
        else:
            raise ValueError("Введите угол или тригонометрическое значение")
    
    angle_val = float(angle) if angle else None
    sin_input = float(sin_val) if sin_val else None
    cos_input = float(cos_val) if cos_val else None
    tan_input = float(tan_val) if tan_val else None
    
    if unknown == 'angle':
        # Ищем угол по sin, cos или tan
        if sin_input is not None:
            if abs(sin_input) > 1:
                raise ValueError("sin не может быть больше 1 или меньше -1")
            angle_val = math.degrees(math.asin(sin_input))
            steps = [
                f"Дано: sin(α) = {sin_input}",
                f"α = arcsin({sin_input}) = {angle_val:.2f}°",
            ]
        elif cos_input is not None:
            if abs(cos_input) > 1:
                raise ValueError("cos не может быть больше 1 или меньше -1")
            angle_val = math.degrees(math.acos(cos_input))
            steps = [
                f"Дано: cos(α) = {cos_input}",
                f"α = arccos({cos_input}) = {angle_val:.2f}°",
            ]
        elif tan_input is not None:
            angle_val = math.degrees(math.atan(tan_input))
            steps = [
                f"Дано: tan(α) = {tan_input}",
                f"α = arctan({tan_input}) = {angle_val:.2f}°",
            ]
        else:
            raise ValueError("Введите sin, cos или tan для нахождения угла")
        
        result = {'α': f'{angle_val:.2f}°'}
        result['sin'] = f'{math.sin(math.radians(angle_val)):.4f}'
        result['cos'] = f'{math.cos(math.radians(angle_val)):.4f}'
        result['tan'] = f'{math.tan(math.radians(angle_val)):.4f}'
        return result, steps, "Тригонометрические функции вычисляются по единичной окружности"
    
    elif unknown == 'sin':
        if angle_val is None:
            raise ValueError("Для нахождения sin нужен угол")
        angle_rad = math.radians(angle_val)
        sin_result = math.sin(angle_rad)
        steps = [
            f"Угол: α = {angle_val}° = {math.radians(angle_val):.4f} рад",
            f"sin({angle_val}°) = {sin_result:.4f}",
        ]
        result = {'sin': f'{sin_result:.4f}'}
        result['cos'] = f'{math.cos(angle_rad):.4f}'
        result['tan'] = f'{math.tan(angle_rad):.4f}'
        result['α'] = f'{angle_val}°'
        return result, steps, "Тригонометрические функции вычисляются по единичной окружности"
    
    elif unknown == 'cos':
        if angle_val is None:
            raise ValueError("Для нахождения cos нужен угол")
        angle_rad = math.radians(angle_val)
        cos_result = math.cos(angle_rad)
        steps = [
            f"Угол: α = {angle_val}° = {math.radians(angle_val):.4f} рад",
            f"cos({angle_val}°) = {cos_result:.4f}",
        ]
        result = {'cos': f'{cos_result:.4f}'}
        result['sin'] = f'{math.sin(angle_rad):.4f}'
        result['tan'] = f'{math.tan(angle_rad):.4f}'
        result['α'] = f'{angle_val}°'
        return result, steps, "Тригонометрические функции вычисляются по единичной окружности"
    
    elif unknown == 'tan':
        if angle_val is None:
            raise ValueError("Для нахождения tan нужен угол")
        angle_rad = math.radians(angle_val)
        tan_result = math.tan(angle_rad) if math.cos(angle_rad) != 0 else None
        steps = [
            f"Угол: α = {angle_val}° = {math.radians(angle_val):.4f} рад",
        ]
        if tan_result is not None:
            steps.append(f"tan({angle_val}°) = {tan_result:.4f}")
        else:
            steps.append(f"tan({angle_val}°) = не определено (cos = 0)")
        
        result = {}
        result['sin'] = f'{math.sin(angle_rad):.4f}'
        result['cos'] = f'{math.cos(angle_rad):.4f}'
        result['α'] = f'{angle_val}°'
        if tan_result is not None:
            result['tan'] = f'{tan_result:.4f}'
        else:
            result['tan'] = 'не определено'
        return result, steps, "Тригонометрические функции вычисляются по единичной окружности"


def solve_law_of_cosines(data):
    """Теорема косинусов"""
    import math
    unknown = data.get('unknown', '').strip()
    a = data.get('a', '').strip()
    b = data.get('b', '').strip()
    gamma = data.get('gamma', '').strip()
    c = data.get('c', '').strip()
    
    # Fallback для задач без выбора unknown
    if not unknown:
        filled = [k for k, v in [('a', a), ('b', b), ('gamma', gamma), ('c', c)] if v]
        if len(filled) == 3:
            missing = ['a', 'b', 'gamma', 'c']
            for m in missing:
                if m not in filled:
                    unknown = m
                    break
        else:
            unknown = 'c'
    
    if not unknown:
        raise ValueError("Выберите, что нужно найти!")
    
    a_val = float(a) if a else None
    b_val = float(b) if b else None
    gamma_val = float(gamma) if gamma else None
    c_val = float(c) if c else None
    
    if unknown == 'c':
        # c² = a² + b² - 2ab·cos(γ)
        if a_val is None or b_val is None or gamma_val is None:
            raise ValueError("Для нахождения стороны c нужны a, b и угол γ")
        gamma_rad = math.radians(gamma_val)
        c_val = (a_val**2 + b_val**2 - 2*a_val*b_val*math.cos(gamma_rad))**0.5
        steps = [
            f"Дано: a={a_val}, b={b_val}, γ={gamma_val}°",
            f"γ в радианах: {math.radians(gamma_val):.4f} рад",
            f"c² = a² + b² - 2ab·cos(γ)",
            f"c² = {a_val}² + {b_val}² - 2·{a_val}·{b_val}·cos({gamma_val}°)",
            f"c² = {a_val**2} + {b_val**2} - {2*a_val*b_val}·{math.cos(gamma_rad):.4f}",
            f"c² = {a_val**2 + b_val**2 - 2*a_val*b_val*math.cos(gamma_rad):.4f}",
            f"c = √{a_val**2 + b_val**2 - 2*a_val*b_val*math.cos(gamma_rad):.4f} = {c_val:.2f}",
        ]
        return {'c': f'{c_val:.2f}'}, steps, "Теорема косинусов: c² = a² + b² - 2ab·cos(γ)"
    
    elif unknown == 'a':
        # a² = c² - b² + 2bc·cos(γ)
        if c_val is None or b_val is None or gamma_val is None:
            raise ValueError("Для нахождения стороны a нужны c, b и угол γ")
        gamma_rad = math.radians(gamma_val)
        a_squared = c_val**2 - b_val**2 + 2*b_val*c_val*math.cos(gamma_rad)
        if a_squared <= 0:
            raise ValueError("Некорректные данные: подкоренное выражение отрицательное")
        a_val = a_squared**0.5
        steps = [
            f"Дано: c={c_val}, b={b_val}, γ={gamma_val}°",
            f"a² = c² - b² + 2bc·cos(γ)",
            f"a² = {c_val}² - {b_val}² + 2·{b_val}·{c_val}·cos({gamma_val}°)",
            f"a² = {c_val**2} - {b_val**2} + {2*b_val*c_val}·{math.cos(gamma_rad):.4f}",
            f"a² = {a_squared:.4f}",
            f"a = √{a_squared:.4f} = {a_val:.2f}",
        ]
        return {'a': f'{a_val:.2f}'}, steps, "Теорема косинусов: a² = c² + b² - 2bc·cos(γ)"
    
    elif unknown == 'b':
        # b² = c² - a² + 2ac·cos(γ)
        if c_val is None or a_val is None or gamma_val is None:
            raise ValueError("Для нахождения стороны b нужны c, a и угол γ")
        gamma_rad = math.radians(gamma_val)
        b_squared = c_val**2 - a_val**2 + 2*a_val*c_val*math.cos(gamma_rad)
        if b_squared <= 0:
            raise ValueError("Некорректные данные: подкоренное выражение отрицательное")
        b_val = b_squared**0.5
        steps = [
            f"Дано: c={c_val}, a={a_val}, γ={gamma_val}°",
            f"b² = c² - a² + 2ac·cos(γ)",
            f"b² = {c_val}² - {a_val}² + 2·{a_val}·{c_val}·cos({gamma_val}°)",
            f"b² = {c_val**2} - {a_val**2} + {2*a_val*c_val}·{math.cos(gamma_rad):.4f}",
            f"b² = {b_squared:.4f}",
            f"b = √{b_squared:.4f} = {b_val:.2f}",
        ]
        return {'b': f'{b_val:.2f}'}, steps, "Теорема косинусов: b² = c² + a² - 2ac·cos(γ)"
    
    elif unknown == 'gamma':
        # cos(γ) = (a² + b² - c²) / (2ab)
        if a_val is None or b_val is None or c_val is None:
            raise ValueError("Для нахождения угла γ нужны все три стороны")
        if a_val == 0 or b_val == 0:
            raise ValueError("Стороны не могут быть равны 0")
        cos_gamma = (a_val**2 + b_val**2 - c_val**2) / (2*a_val*b_val)
        if abs(cos_gamma) > 1:
            raise ValueError("Некорректные данные: cos не может быть больше 1 или меньше -1")
        gamma_val = math.degrees(math.acos(cos_gamma))
        steps = [
            f"Дано: a={a_val}, b={b_val}, c={c_val}",
            f"cos(γ) = (a² + b² - c²) / (2ab)",
            f"cos(γ) = ({a_val}² + {b_val}² - {c_val}²) / (2·{a_val}·{b_val})",
            f"cos(γ) = ({a_val**2} + {b_val**2} - {c_val**2}) / {2*a_val*b_val}",
            f"cos(γ) = {cos_gamma:.4f}",
            f"γ = arccos({cos_gamma:.4f}) = {gamma_val:.2f}°",
        ]
        return {'γ': f'{gamma_val:.2f}°'}, steps, "Теорема косинусов: cos(γ) = (a² + b² - c²) / (2ab)"


def solve_right_triangle(data):
    """Решение прямоугольного треугольника по известным элементам"""
    import math
    
    unknown = data.get('unknown', '').strip()
    a = data.get('a', '').strip()
    b = data.get('b', '').strip()
    c = data.get('c', '').strip()
    alpha = data.get('alpha', '').strip()
    
    # Fallback для задач без выбора unknown
    if not unknown:
        filled = [k for k, v in [('a', a), ('b', b), ('c', c), ('alpha', alpha)] if v]
        if len(filled) >= 2:
            missing = ['a', 'b', 'c', 'alpha']
            for m in missing:
                if m not in filled:
                    unknown = m
                    break
        else:
            unknown = 'c'
    
    if not unknown:
        raise ValueError("Выберите, что нужно найти!")
    
    a_val = float(a) if a else None
    b_val = float(b) if b else None
    c_val = float(c) if c else None
    alpha_val = float(alpha) if alpha else None
    
    # Если unknown не определён fallback'ом, определяем по заполненным полям
    if not unknown:
        if a_val is not None and b_val is not None:
            unknown = 'c'
        elif a_val is not None and c_val is not None:
            unknown = 'b'
        elif b_val is not None and c_val is not None:
            unknown = 'a'
        else:
            unknown = 'c'
    
    steps = []
    results = {}
    
    # Считаем известные величины
    known_sides = sum(1 for v in [a_val, b_val, c_val] if v is not None)
    has_angle = alpha_val is not None
    
    if known_sides < 2 and not (known_sides == 1 and has_angle):
        raise ValueError("Недостаточно данных. Введите минимум 2 стороны ИЛИ 1 сторону и угол.")
    
    # Если угол задан, используем его для вычисления сторон
    if has_angle:
        alpha_rad = math.radians(alpha_val)
        
        if a_val is None and b_val is not None:
            # a = b * tan(α)
            a_val = b_val * math.tan(alpha_rad)
            steps.append(f"Находим a: a = b · tan(α) = {b_val} · tan({alpha_val}°) = {a_val:.4f}")
        
        elif b_val is None and a_val is not None:
            # b = a / tan(α)
            b_val = a_val / math.tan(alpha_rad)
            steps.append(f"Находим b: b = a / tan(α) = {a_val} / tan({alpha_val}°) = {b_val:.4f}")
        
        elif c_val is None and a_val is not None:
            # c = a / sin(α)
            c_val = a_val / math.sin(alpha_rad)
            steps.append(f"Находим c: c = a / sin(α) = {a_val} / sin({alpha_val}°) = {c_val:.4f}")
        
        elif c_val is not None and a_val is None:
            # a = c * sin(α)
            a_val = c_val * math.sin(alpha_rad)
            steps.append(f"Находим a: a = c · sin(α) = {c_val} · sin({alpha_val}°) = {a_val:.4f}")
        
        elif c_val is not None and b_val is None:
            # b = c * cos(α)
            b_val = c_val * math.cos(alpha_rad)
            steps.append(f"Находим b: b = c · cos(α) = {c_val} · cos({alpha_val}°) = {b_val:.4f}")
        
        elif a_val is not None and b_val is not None:
            # Находим гипотенузу
            c_val = (a_val**2 + b_val**2)**0.5
            steps.append(f"Находим c по теореме Пифагора: c = √(a² + b²) = √({a_val}² + {b_val}²) = {c_val:.4f}")
    
    # Если угол НЕ задан, вычисляем его
    if not has_angle:
        # Шаг 1: Находим неизвестные стороны по теореме Пифагора
        if a_val is None and b_val is not None and c_val is not None:
            if c_val <= b_val:
                raise ValueError("Гипотенуза должна быть больше катета")
            a_val = (c_val**2 - b_val**2)**0.5
            steps.append(f"Находим a по теореме Пифагора: a = √(c² - b²) = √({c_val}² - {b_val}²) = {a_val:.4f}")
        
        elif b_val is None and a_val is not None and c_val is not None:
            if c_val <= a_val:
                raise ValueError("Гипотенуза должна быть больше катета")
            b_val = (c_val**2 - a_val**2)**0.5
            steps.append(f"Находим b по теореме Пифагора: b = √(c² - a²) = √({c_val}² - {a_val}²) = {b_val:.4f}")
        
        elif c_val is None and a_val is not None and b_val is not None:
            c_val = (a_val**2 + b_val**2)**0.5
            steps.append(f"Находим c по теореме Пифагора: c = √(a² + b²) = √({a_val}² + {b_val}²) = {c_val:.4f}")
        
        # Шаг 2: Находим углы по тригонометрии
        if a_val is not None and c_val is not None:
            sin_alpha = a_val / c_val
            if abs(sin_alpha) > 1:
                raise ValueError("Некорректные данные: sin не может быть > 1")
            alpha_val = math.degrees(math.asin(sin_alpha))
            steps.append(f"Находим α: sin(α) = a/c = {a_val:.4f}/{c_val:.4f} = {sin_alpha:.4f}")
            steps.append(f"α = arcsin({sin_alpha:.4f}) = {alpha_val:.2f}°")
        
        elif a_val is not None and b_val is not None:
            tan_alpha = a_val / b_val
            alpha_val = math.degrees(math.atan(tan_alpha))
            steps.append(f"Находим α: tan(α) = a/b = {a_val:.4f}/{b_val:.4f} = {tan_alpha:.4f}")
            steps.append(f"α = arctan({tan_alpha:.4f}) = {alpha_val:.2f}°")
        
        elif b_val is not None and c_val is not None:
            cos_alpha = b_val / c_val
            if abs(cos_alpha) > 1:
                raise ValueError("Некорректные данные: cos не может быть > 1")
            alpha_val = math.degrees(math.acos(cos_alpha))
            steps.append(f"Находим α: cos(α) = b/c = {b_val:.4f}/{c_val:.4f} = {cos_alpha:.4f}")
            steps.append(f"α = arccos({cos_alpha:.4f}) = {alpha_val:.2f}°")
    
    # Шаг 3: Находим второй угол
    beta_val = 90 - alpha_val
    if has_angle:
        steps.append(f"Находим β: β = 90° - α = 90° - {alpha_val:.2f}° = {beta_val:.2f}°")
    else:
        steps.append(f"Находим β: β = 90° - α = {beta_val:.2f}°")
    
    # Формируем результаты
    if a_val is not None:
        results['a'] = f'{a_val:.2f}'
    if b_val is not None:
        results['b'] = f'{b_val:.2f}'
    if c_val is not None:
        results['c'] = f'{c_val:.2f}'
    results['α'] = f'{alpha_val:.2f}°'
    results['β'] = f'{beta_val:.2f}°'
    
    explanation = "Прямоугольный треугольник решается по теореме Пифагора и тригонометрическим функциям. Сумма острых углов = 90°."
    
    return results, steps, explanation


# ===== ФУНКЦИИ ДЛЯ АНАЛИЗА =====

def solve_derivative_power(data):
    """Производная степени: f(x) = xⁿ"""
    import math
    n = float(data.get('n', '0'))
    x = float(data.get('x', '0'))
    
    # f'(x) = n * x^(n-1)
    if x == 0 and n - 1 < 0:
        raise ValueError("Производная не определена в точке x = 0")
    
    derivative = n * (x ** (n - 1))
    steps = [
        f"Дано: f(x) = x^{n}",
        f"f'(x) = n · xⁿ⁻¹ = {n} · x^{n-1}",
        f"f'({x}) = {n} · ({x})^{n-1} = {derivative:.4f}",
    ]
    return {'f\'(x)': f'{derivative:.4f}'}, steps, "Производная степени: d/dx(xⁿ) = n·xⁿ⁻¹"


def solve_integral_power(data):
    """Определённый интеграл: ∫(xⁿ) dx от a до b"""
    import math
    n = float(data.get('n', '0'))
    a = float(data.get('a', '0'))
    b = float(data.get('b', '0'))
    
    if n == -1:
        raise ValueError("Для n = -1 используется ln|x|")
    
    # F(x) = xⁿ⁺¹/(n+1)
    F_a = (a ** (n + 1)) / (n + 1)
    F_b = (b ** (n + 1)) / (n + 1)
    result = F_b - F_a
    
    steps = [
        f"Дано: ∫(x^{n}) dx от {a} до {b}",
        f"Первообразная: F(x) = xⁿ⁺¹/(n+1) = x^{n+1}/{n+1}",
        f"F({b}) = {b}^{n+1}/{n+1} = {F_b:.4f}",
        f"F({a}) = {a}^{n+1}/{n+1} = {F_a:.4f}",
        f"∫ = F({b}) - F({a}) = {F_b:.4f} - {F_a:.4f} = {result:.4f}",
    ]
    return {'∫': f'{result:.4f}'}, steps, "Определённый интеграл вычисляется по формуле Ньютона-Лейбница"


def solve_limit(data):
    """Предел функции — замечательные пределы"""
    import math
    limit_type = data.get('type', '').strip().lower()
    
    if limit_type in ['sinx', 'sin(x)/x', 'sin']:
        # lim(x→0) sin(x)/x = 1
        steps = [
            "lim(x→0) sin(x)/x",
            "Это первый замечательный предел",
            "lim(x→0) sin(x)/x = 1",
        ]
        return {'lim': '1'}, steps, "Первый замечательный предел: lim(x→0) sin(x)/x = 1"
    
    elif limit_type in ['exp', '(1+1/x)^x', 'euler', 'число e']:
        # lim(x→∞) (1+1/x)^x = e
        steps = [
            "lim(x→∞) (1+1/x)ˣ",
            "Это определение числа Эйлера (второй замечательный предел)",
            "lim(x→∞) (1+1/x)ˣ = e ≈ 2.71828",
        ]
        return {'lim': '2.71828'}, steps, "Второй замечательный предел: lim(x→∞) (1+1/x)ˣ = e"
    
    else:
        raise ValueError("Укажите тип предела: 'sin' (sin(x)/x) или 'euler' ((1+1/x)^x)")


# ===== ФУНКЦИИ ДЛЯ ВЕКТОРОВ =====

def solve_vector_addition(data):
    """Сложение векторов"""
    import math
    a = float(data.get('a', '0'))
    b = float(data.get('b', '0'))
    angle = float(data.get('angle', '0'))
    
    angle_rad = math.radians(angle)
    
    # |a + b| = √(a² + b² + 2ab·cos(γ))
    result = (a**2 + b**2 + 2*a*b*math.cos(angle_rad))**0.5
    
    # Угол между суммой и вектором a
    # tan(α) = b·sin(γ) / (a + b·cos(γ))
    denominator = a + b * math.cos(angle_rad)
    if abs(denominator) > 1e-10:
        alpha = math.degrees(math.atan2(b * math.sin(angle_rad), denominator))
    else:
        alpha = 90.0
    
    steps = [
        f"Дано: |a| = {a}, |b| = {b}, γ = {angle}°",
        f"γ в радианах: {angle_rad:.4f} рад",
        f"|a + b| = √(a² + b² + 2ab·cos(γ))",
        f"|a + b| = √({a}² + {b}² + 2·{a}·{b}·cos({angle}°))",
        f"|a + b| = √({a**2} + {b**2} + {2*a*b}·{math.cos(angle_rad):.4f})",
        f"|a + b| = √{a**2 + b**2 + 2*a*b*math.cos(angle_rad):.4f} = {result:.2f}",
        f"Угол α между суммой и вектором a: α = {alpha:.2f}°",
    ]
    return {
        '|a+b|': f'{result:.2f}',
        'α': f'{alpha:.2f}°'
    }, steps, "Сложение векторов: модуль суммы находится по теореме косинусов"


def solve_scalar_product(data):
    """Скалярное произведение"""
    import math
    a = float(data.get('a', '0'))
    b = float(data.get('b', '0'))
    angle = float(data.get('angle', '0'))
    
    angle_rad = math.radians(angle)
    scalar = a * b * math.cos(angle_rad)
    
    steps = [
        f"Дано: |a| = {a}, |b| = {b}, γ = {angle}°",
        f"a · b = |a| · |b| · cos(γ)",
        f"a · b = {a} · {b} · cos({angle}°)",
        f"a · b = {a*b} · {math.cos(angle_rad):.4f} = {scalar:.4f}",
    ]
    
    # Проверка: если скалярное = 0, векторы перпендикулярны
    if abs(scalar) < 1e-6:
        steps.append("a · b ≈ 0 → векторы перпендикулярны (γ = 90°)")
    
    return {'a·b': f'{scalar:.4f}'}, steps, "Скалярное произведение: a·b = |a|·|b|·cos(γ)"


def solve_projection(data):
    """Проекция вектора"""
    import math
    a = float(data.get('a', '0'))
    angle = float(data.get('angle', '0'))
    
    angle_rad = math.radians(angle)
    projection = a * math.cos(angle_rad)
    
    steps = [
        f"Дано: |a| = {a}, |b| = {b}, γ = {angle}°",
        f"Pr_b(a) = |a| · cos(γ)",
        f"Pr_b(a) = {a} · cos({angle}°)",
        f"Pr_b(a) = {a} · {math.cos(angle_rad):.4f} = {projection:.4f}",
    ]
    
    if projection > 0:
        steps.append("Проекция положительна → острый угол между векторами")
    elif projection < 0:
        steps.append("Проекция отрицательна → тупой угол между векторами")
    else:
        steps.append("Проекция равна 0 → векторы перпендикулярны")
    
    return {'Pr_b(a)': f'{projection:.4f}'}, steps, "Проекция вектора: Pr_b(a) = |a|·cos(γ)"


# ===== ФУНКЦИИ ДЛЯ ТЕОРИИ ВЕРОЯТНОСТЕЙ =====

def solve_probability_classic(data):
    """Классическая вероятность"""
    m = int(data.get('m', '0'))
    n = int(data.get('n', '1'))
    
    if n == 0:
        raise ValueError("Общее число исходов не может быть 0")
    if m < 0 or m > n:
        raise ValueError("m должно быть в диапазоне [0, n]")
    
    probability = m / n
    percentage = probability * 100
    
    steps = [
        f"Дано: m = {m} (благоприятные), n = {n} (все исходы)",
        f"P = m / n = {m} / {n} = {probability:.4f}",
        f"P = {percentage:.2f}%",
    ]
    return {
        'P': f'{probability:.4f}',
        'P(%)': f'{percentage:.2f}%'
    }, steps, "Классическая вероятность: P = m/n"


def solve_combinatorics(data):
    """Комбинаторика: перестановки, размещения, сочетания"""
    import math
    n = int(data.get('n', '0'))
    k = int(data.get('k', '0'))
    method = data.get('method', 'combination').strip().lower()
    
    if k < 0 or k > n:
        raise ValueError("k должно быть в диапазоне [0, n]")
    
    if method in ['permutation', 'p', 'перестановк']:
        # P(n) = n!
        count = math.factorial(n)
        formula = f"P({n}) = {n}!"
        steps = [
            f"Метод: перестановки",
            f"Формула: P(n) = n!",
            f"{formula} = {count}",
        ]
    
    elif method in ['arrangement', 'a', 'размещение']:
        # A(n,k) = n!/(n-k)!
        count = math.factorial(n) // math.factorial(n - k)
        formula = f"A({n},{k})"
        steps = [
            f"Метод: размещения",
            f"Формула: A(n,k) = n!/(n-k)!",
            f"{formula} = {n}! / ({n}-{k})! = {n}! / {n-k}!",
            f"{formula} = {math.factorial(n)} / {math.factorial(n-k)} = {count}",
        ]
    
    elif method in ['combination', 'c', 'сочетание']:
        # C(n,k) = n!/(k!(n-k)!)
        count = math.comb(n, k)
        formula = f"C({n},{k})"
        steps = [
            f"Метод: сочетания",
            f"Формула: C(n,k) = n!/(k!(n-k)!)",
            f"{formula} = {n}! / ({k}! · {n-k}!)",
            f"{formula} = {math.factorial(n)} / ({math.factorial(k)} · {math.factorial(n-k)}) = {count}",
        ]
    
    else:
        raise ValueError("Неизвестный метод. Используйте: permutation, arrangement, combination")
    
    return {
        'count': str(count),
        'formula': formula
    }, steps, f"Комбинаторика: {formula} = {count}"


def solve_probability_distribution(data):
    """Формула Бернулли (биномиальное распределение)"""
    import math
    n = int(data.get('n', '0'))
    k = int(data.get('k', '0'))
    p = float(data.get('p', '0'))
    
    if n <= 0:
        raise ValueError("n должно быть > 0")
    if k < 0 or k > n:
        raise ValueError("k должно быть в диапазоне [0, n]")
    if p < 0 or p > 1:
        raise ValueError("p должно быть в диапазоне [0, 1]")
    
    # C(n,k) * p^k * (1-p)^(n-k)
    c_nk = math.comb(n, k)
    prob = c_nk * (p ** k) * ((1 - p) ** (n - k))
    expected = n * p
    
    steps = [
        f"Дано: n = {n} (испытаний), k = {k} (успехов), p = {p}",
        f"Формула Бернулли: P(k,n) = C(n,k) · pᵏ · (1-p)ⁿ⁻ᵏ",
        f"C({n},{k}) = {c_nk}",
        f"pᵏ = {p}^{k} = {p**k:.6f}",
        f"(1-p)ⁿ⁻ᵏ = {1-p}^{n-k} = {(1-p)**(n-k):.6f}",
        f"P({k},{n}) = {c_nk} · {p**k:.6f} · {(1-p)**(n-k):.6f} = {prob:.6f}",
        f"Мат. ожидание: M = n·p = {n}·{p} = {expected:.2f}",
    ]
    return {
        'P(k,n)': f'{prob:.6f}',
        'M': f'{expected:.2f}',
        'D': f'{n * p * (1-p):.4f}',
    }, steps, "Формула Бернулли: P(k,n) = C(n,k) · pᵏ · (1-p)ⁿ⁻ᵏ"
