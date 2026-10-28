# tasks.py
import matplotlib
matplotlib.use('Agg') # Чтобы графики строились без открытия окон
import matplotlib.pyplot as plt
import io
import base64
import os


TASKS = {}


# ============================================================
# 1. Кинематика: Равноускоренное движение
# ============================================================
def solve_kinematics(known, target):
    v0, v, a, t, s = known.get('v0'), known.get('v'), known.get('a'), known.get('t'), known.get('s')
    explanation = "Равноускоренное движение: v = v₀ + a·t, s = v₀·t + a·t²/2, s = (v₀ + v)·t/2."

    if target == 'v':
        if v0 is not None and a is not None and t is not None:
            val = v0 + a * t
            steps = ["Формула: v = v₀ + a·t", f"v = {v0} + {a}·{t} = {val:.3f} м/с"]
        elif v0 is not None and s is not None and t is not None and t != 0:
            val = 2 * s / t - v0
            steps = ["Из s = (v₀ + v)·t/2: v = 2s/t - v₀", f"v = 2·{s}/{t} - {v0} = {val:.3f} м/с"]
        else:
            raise ValueError("Для поиска v нужны (v₀, a, t) или (v₀, s, t)")
        return {"v": f"{val:.3f} м/с"}, steps, explanation

    if target == 'a':
        if v0 is not None and v is not None and t is not None and t != 0:
            val = (v - v0) / t
            steps = ["Из v = v₀ + a·t: a = (v - v₀)/t", f"a = ({v} - {v0})/{t} = {val:.3f} м/с²"]
        elif v is not None and s is not None and t is not None and t != 0:
            val = 2 * (v * t - s) / (t * t)
            steps = ["Из s = v·t - a·t²/2: a = 2(v·t - s)/t²", f"a = 2·({v}·{t} - {s})/{t}² = {val:.3f} м/с²"]
        elif v0 is not None and s is not None and t is not None and t != 0:
            val = 2 * (s - v0 * t) / (t * t)
            steps = ["Из s = v₀·t + a·t²/2: a = 2(s - v₀·t)/t²", f"a = 2·({s} - {v0}·{t})/{t}² = {val:.3f} м/с²"]
        else:
            raise ValueError("Для поиска a нужны (v₀, v, t), (v, s, t) или (v₀, s, t)")
        return {"a": f"{val:.3f} м/с²"}, steps, explanation

    if target == 't':
        if v0 is not None and v is not None and a is not None and a != 0:
            val = (v - v0) / a
            steps = ["Из v = v₀ + a·t: t = (v - v₀)/a", f"t = ({v} - {v0})/{a} = {val:.3f} с"]
        elif v0 is not None and a is not None and s is not None:
            disc = v0 ** 2 + 2 * a * s
            if disc < 0: raise ValueError("Нет решения: подкоренное выражение отрицательно")
            val = (-v0 + disc ** 0.5) / a
            steps = ["Из s = v₀·t + a·t²/2: t = (-v₀ + √(v₀² + 2·a·s)) / a",
                     f"t = (-{v0} + √({v0}² + 2·{a}·{s})) / {a} = {val:.3f} с"]
        else:
            raise ValueError("Для поиска t нужны (v₀, v, a) или (v₀, a, s)")
        return {"t": f"{val:.3f} с"}, steps, explanation

    if target == 's':
        if v0 is not None and a is not None and t is not None:
            val = v0 * t + 0.5 * a * t * t
            steps = ["Формула: s = v₀·t + a·t²/2", f"s = {v0}·{t} + {a}·{t}²/2 = {val:.3f} м"]
        elif v0 is not None and v is not None and t is not None:
            val = (v0 + v) / 2 * t
            steps = ["Формула: s = (v₀ + v)·t/2", f"s = ({v0} + {v})·{t}/2 = {val:.3f} м"]
        else:
            raise ValueError("Для поиска s нужны (v₀, a, t) или (v₀, v, t)")
        return {"s": f"{val:.3f} м"}, steps, explanation

    raise ValueError("Неизвестная цель")


TASKS['kinematics'] = {
    "name": "Равноускоренное движение",
    "category": "Кинематика",
    "icon": "🚀",
    "image": "/static/img/kinematics.svg",
    "quantities": {
        "v0": ("Начальная скорость v₀", "м/с"),
        "v": ("Конечная скорость v", "м/с"),
        "a": ("Ускорение a", "м/с²"),
        "t": ("Время t", "с"),
        "s": ("Путь s", "м"),
    },
    "targets": {
        "v": "Конечную скорость v",
        "a": "Ускорение a",
        "t": "Время t",
        "s": "Путь s",
    },
    "solve": solve_kinematics,
}


# ============================================================
# 2. Динамика: Второй закон Ньютона
# ============================================================
def solve_newton(known, target):
    m, F, a = known.get('m'), known.get('F'), known.get('a')
    explanation = "Второй закон Ньютона: F = m·a."

    if target == 'F':
        if m is not None and a is not None:
            val = m * a
            steps = ["Формула: F = m·a", f"F = {m}·{a} = {val:.3f} Н"]
        else:
            raise ValueError("Для поиска F нужны m и a")
        return {"F": f"{val:.3f} Н"}, steps, explanation

    if target == 'm':
        if F is not None and a is not None and a != 0:
            val = F / a
            steps = ["Из F = m·a: m = F/a", f"m = {F}/{a} = {val:.3f} кг"]
        else:
            raise ValueError("Для поиска m нужны F и a (a ≠ 0)")
        return {"m": f"{val:.3f} кг"}, steps, explanation

    if target == 'a':
        if F is not None and m is not None and m != 0:
            val = F / m
            steps = ["Из F = m·a: a = F/m", f"a = {F}/{m} = {val:.3f} м/с²"]
        else:
            raise ValueError("Для поиска a нужны F и m (m ≠ 0)")
        return {"a": f"{val:.3f} м/с²"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['newton'] = {
    "name": "Второй закон Ньютона",
    "category": "Динамика",
    "icon": "⚙️",
    "image": "/static/img/newton.svg",
    "quantities": {
        "m": ("Масса m", "кг"),
        "F": ("Сила F", "Н"),
        "a": ("Ускорение a", "м/с²"),
    },
    "targets": {
        "F": "Силу F",
        "m": "Массу m",
        "a": "Ускорение a",
    },
    "solve": solve_newton,
}


# ============================================================
# 3. Электричество: Закон Ома
# ============================================================
def solve_ohm(known, target):
    U, R, I = known.get('U'), known.get('R'), known.get('I')
    explanation = "Закон Ома для участка цепи: I = U/R."

    if target == 'I':
        if U is not None and R is not None and R != 0:
            val = U / R
            steps = ["Формула: I = U/R", f"I = {U}/{R} = {val:.4f} А"]
        else:
            raise ValueError("Для поиска I нужны U и R (R ≠ 0)")
        return {"I": f"{val:.4f} А"}, steps, explanation

    if target == 'U':
        if I is not None and R is not None:
            val = I * R
            steps = ["Из I = U/R: U = I·R", f"U = {I}·{R} = {val:.3f} В"]
        else:
            raise ValueError("Для поиска U нужны I и R")
        return {"U": f"{val:.3f} В"}, steps, explanation

    if target == 'R':
        if U is not None and I is not None and I != 0:
            val = U / I
            steps = ["Из I = U/R: R = U/I", f"R = {U}/{I} = {val:.3f} Ом"]
        else:
            raise ValueError("Для поиска R нужны U и I (I ≠ 0)")
        return {"R": f"{val:.3f} Ом"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['ohm'] = {
    "name": "Закон Ома",
    "category": "Электричество",
    "icon": "🔌",
    "image": "/static/img/ohm.svg",
    "quantities": {
        "U": ("Напряжение U", "В"),
        "R": ("Сопротивление R", "Ом"),
        "I": ("Сила тока I", "А"),
    },
    "targets": {
        "I": "Силу тока I",
        "U": "Напряжение U",
        "R": "Сопротивление R",
    },
    "solve": solve_ohm,
}


# ============================================================
# 4. Энергия: Механическая работа
# ============================================================
def solve_work(known, target):
    F, s, A = known.get('F'), known.get('s'), known.get('A')
    explanation = "Механическая работа: A = F·s."

    if target == 'A':
        if F is not None and s is not None:
            val = F * s
            steps = ["Формула: A = F·s", f"A = {F}·{s} = {val:.3f} Дж"]
        else:
            raise ValueError("Для поиска A нужны F и s")
        return {"A": f"{val:.3f} Дж"}, steps, explanation

    if target == 'F':
        if A is not None and s is not None and s != 0:
            val = A / s
            steps = ["Из A = F·s: F = A/s", f"F = {A}/{s} = {val:.3f} Н"]
        else:
            raise ValueError("Для поиска F нужны A и s (s ≠ 0)")
        return {"F": f"{val:.3f} Н"}, steps, explanation

    if target == 's':
        if A is not None and F is not None and F != 0:
            val = A / F
            steps = ["Из A = F·s: s = A/F", f"s = {A}/{F} = {val:.3f} м"]
        else:
            raise ValueError("Для поиска s нужны A и F (F ≠ 0)")
        return {"s": f"{val:.3f} м"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['work'] = {
    "name": "Механическая работа",
    "category": "Энергия",
    "icon": "💪",
    "image": "/static/img/work.svg",
    "quantities": {
        "F": ("Сила F", "Н"),
        "s": ("Перемещение s", "м"),
        "A": ("Работа A", "Дж"),
    },
    "targets": {
        "A": "Работу A",
        "F": "Силу F",
        "s": "Перемещение s",
    },
    "solve": solve_work,
}


# ============================================================
# 5. Энергия: Кинетическая энергия
# ============================================================
def solve_energy(known, target):
    m, v, E = known.get('m'), known.get('v'), known.get('E')
    explanation = "Кинетическая энергия: E = m·v²/2."

    if target == 'E':
        if m is not None and v is not None:
            val = m * v * v / 2
            steps = ["Формула: E = m·v²/2", f"E = {m}·{v}²/2 = {val:.3f} Дж"]
        else:
            raise ValueError("Для поиска E нужны m и v")
        return {"E": f"{val:.3f} Дж"}, steps, explanation

    if target == 'm':
        if E is not None and v is not None and v != 0:
            val = 2 * E / (v * v)
            steps = ["Из E = m·v²/2: m = 2·E/v²", f"m = 2·{E}/{v}² = {val:.3f} кг"]
        else:
            raise ValueError("Для поиска m нужны E и v (v ≠ 0)")
        return {"m": f"{val:.3f} кг"}, steps, explanation

    if target == 'v':
        if E is not None and m is not None and m != 0:
            val = (2 * E / m) ** 0.5
            steps = ["Из E = m·v²/2: v = √(2·E/m)", f"v = √(2·{E}/{m}) = {val:.3f} м/с"]
        else:
            raise ValueError("Для поиска v нужны E и m (m ≠ 0)")
        return {"v": f"{val:.3f} м/с"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['energy'] = {
    "name": "Кинетическая энергия",
    "category": "Энергия",
    "icon": "⚡",
    "image": "/static/img/energy.svg",
    "quantities": {
        "m": ("Масса m", "кг"),
        "v": ("Скорость v", "м/с"),
        "E": ("Энергия E", "Дж"),
    },
    "targets": {
        "E": "Кинетическую энергию E",
        "m": "Массу m",
        "v": "Скорость v",
    },
    "solve": solve_energy,
}


# ============================================================
# 6. Давление
# ============================================================
def solve_pressure(known, target):
    F, S, p = known.get('F'), known.get('S'), known.get('p')
    explanation = "Давление: p = F/S."

    if target == 'p':
        if F is not None and S is not None and S != 0:
            val = F / S
            steps = ["Формула: p = F/S", f"p = {F}/{S} = {val:.2f} Па"]
        else:
            raise ValueError("Для поиска p нужны F и S (S ≠ 0)")
        return {"p": f"{val:.2f} Па"}, steps, explanation

    if target == 'F':
        if p is not None and S is not None:
            val = p * S
            steps = ["Из p = F/S: F = p·S", f"F = {p}·{S} = {val:.2f} Н"]
        else:
            raise ValueError("Для поиска F нужны p и S")
        return {"F": f"{val:.2f} Н"}, steps, explanation

    if target == 'S':
        if p is not None and F is not None and p != 0:
            val = F / p
            steps = ["Из p = F/S: S = F/p", f"S = {F}/{p} = {val:.4f} м²"]
        else:
            raise ValueError("Для поиска S нужны F и p (p ≠ 0)")
        return {"S": f"{val:.4f} м²"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['pressure'] = {
    "name": "Давление",
    "category": "Давление",
    "icon": "📏",
    "image": "/static/img/pressure.svg",
    "quantities": {
        "F": ("Сила F", "Н"),
        "S": ("Площадь S", "м²"),
        "p": ("Давление p", "Па"),
    },
    "targets": {
        "p": "Давление p",
        "F": "Силу F",
        "S": "Площадь S",
    },
    "solve": solve_pressure,
}


# ============================================================
# 7. Плотность
# ============================================================
def solve_density(known, target):
    m, V, rho = known.get('m'), known.get('V'), known.get('rho')
    explanation = "Плотность: ρ = m/V."

    if target == 'rho':
        if m is not None and V is not None and V != 0:
            val = m / V
            steps = ["Формула: ρ = m/V", f"ρ = {m}/{V} = {val:.3f} кг/м³"]
        else:
            raise ValueError("Для поиска ρ нужны m и V (V ≠ 0)")
        return {"rho": f"{val:.3f} кг/м³"}, steps, explanation

    if target == 'm':
        if rho is not None and V is not None:
            val = rho * V
            steps = ["Из ρ = m/V: m = ρ·V", f"m = {rho}·{V} = {val:.3f} кг"]
        else:
            raise ValueError("Для поиска m нужны ρ и V")
        return {"m": f"{val:.3f} кг"}, steps, explanation

    if target == 'V':
        if rho is not None and m is not None and rho != 0:
            val = m / rho
            steps = ["Из ρ = m/V: V = m/ρ", f"V = {m}/{rho} = {val:.4f} м³"]
        else:
            raise ValueError("Для поиска V нужны m и ρ (ρ ≠ 0)")
        return {"V": f"{val:.4f} м³"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['density'] = {
    "name": "Плотность вещества",
    "category": "Давление",
    "icon": "🧪",
    "image": "/static/img/density.svg",
    "quantities": {
        "m": ("Масса m", "кг"),
        "V": ("Объём V", "м³"),
        "rho": ("Плотность ρ", "кг/м³"),
    },
    "targets": {
        "rho": "Плотность ρ",
        "m": "Массу m",
        "V": "Объём V",
    },
    "solve": solve_density,
}


# ============================================================
# 8. Динамика: Сила тяжести
# ============================================================
def solve_gravity(known, target):
    m, F = known.get('m'), known.get('F')
    g = 9.8
    explanation = "Сила тяжести: F = m·g, где g = 9.8 м/с²."

    if target == 'F':
        if m is not None:
            val = m * g
            steps = ["Формула: F = m·g", f"F = {m}·9.8 = {val:.2f} Н"]
        else:
            raise ValueError("Для поиска F нужна m")
        return {"F": f"{val:.2f} Н"}, steps, explanation

    if target == 'm':
        if F is not None and g != 0:
            val = F / g
            steps = ["Из F = m·g: m = F/g", f"m = {F}/9.8 = {val:.3f} кг"]
        else:
            raise ValueError("Для поиска m нужна F")
        return {"m": f"{val:.3f} кг"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['gravity'] = {
    "name": "Сила тяжести",
    "category": "Динамика",
    "icon": "🌍",
    "image": "/static/img/gravity.svg",
    "quantities": {
        "m": ("Масса m", "кг"),
        "F": ("Сила F", "Н"),
    },
    "targets": {
        "F": "Силу тяжести F",
        "m": "Массу m",
    },
    "solve": solve_gravity,
}


# ============================================================
# 9. Давление: Сила Архимеда
# ============================================================
def solve_archimedes(known, target):
    rho, V, F = known.get('rho'), known.get('V'), known.get('F')
    g = 9.8
    explanation = "Сила Архимеда: F_A = ρ_ж·g·V."

    if target == 'F':
        if rho is not None and V is not None:
            val = rho * g * V
            steps = ["Формула: F_A = ρ·g·V", f"F_A = {rho}·9.8·{V} = {val:.2f} Н"]
        else:
            raise ValueError("Для поиска F_A нужны ρ и V")
        return {"F": f"{val:.2f} Н"}, steps, explanation

    if target == 'V':
        if F is not None and rho is not None and rho != 0:
            val = F / (rho * g)
            steps = ["Из F_A = ρ·g·V: V = F_A/(ρ·g)", f"V = {F}/({rho}·9.8) = {val:.4f} м³"]
        else:
            raise ValueError("Для поиска V нужны F_A и ρ (ρ ≠ 0)")
        return {"V": f"{val:.4f} м³"}, steps, explanation

    if target == 'rho':
        if F is not None and V is not None and V != 0:
            val = F / (g * V)
            steps = ["Из F_A = ρ·g·V: ρ = F_A/(g·V)", f"ρ = {F}/(9.8·{V}) = {val:.2f} кг/м³"]
        else:
            raise ValueError("Для поиска ρ нужны F_A и V (V ≠ 0)")
        return {"rho": f"{val:.2f} кг/м³"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['archimedes'] = {
    "name": "Сила Архимеда",
    "category": "Давление",
    "icon": "🚢",
    "image": "/static/img/archimedes.svg",
    "quantities": {
        "rho": ("Плотность жидкости ρ", "кг/м³"),
        "V": ("Объём тела V", "м³"),
        "F": ("Сила Архимеда F_A", "Н"),
    },
    "targets": {
        "F": "Силу Архимеда F_A",
        "V": "Объём V",
        "rho": "Плотность жидкости ρ",
    },
    "solve": solve_archimedes,
}


# ============================================================
# 10. Энергия: Мощность
# ============================================================
def solve_power(known, target):
    A, t, N = known.get('A'), known.get('t'), known.get('N')
    explanation = "Мощность: N = A/t."

    if target == 'N':
        if A is not None and t is not None and t != 0:
            val = A / t
            steps = ["Формула: N = A/t", f"N = {A}/{t} = {val:.2f} Вт"]
        else:
            raise ValueError("Для поиска N нужны A и t (t ≠ 0)")
        return {"N": f"{val:.2f} Вт"}, steps, explanation

    if target == 'A':
        if N is not None and t is not None:
            val = N * t
            steps = ["Из N = A/t: A = N·t", f"A = {N}·{t} = {val:.2f} Дж"]
        else:
            raise ValueError("Для поиска A нужны N и t")
        return {"A": f"{val:.2f} Дж"}, steps, explanation

    if target == 't':
        if A is not None and N is not None and N != 0:
            val = A / N
            steps = ["Из N = A/t: t = A/N", f"t = {A}/{N} = {val:.2f} с"]
        else:
            raise ValueError("Для поиска t нужны A и N (N ≠ 0)")
        return {"t": f"{val:.2f} с"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['power'] = {
    "name": "Механическая мощность",
    "category": "Энергия",
    "icon": "⚙️",
    "image": "/static/img/power.svg",
    "quantities": {
        "A": ("Работа A", "Дж"),
        "t": ("Время t", "с"),
        "N": ("Мощность N", "Вт"),
    },
    "targets": {
        "N": "Мощность N",
        "A": "Работу A",
        "t": "Время t",
    },
    "solve": solve_power,
}


# ============================================================
# 11. Электричество: Последовательное соединение
# ============================================================
def solve_series(known, target):
    R1, R2, R = known.get('R1'), known.get('R2'), known.get('R')
    explanation = "Последовательное соединение: R = R₁ + R₂."

    if target == 'R':
        if R1 is not None and R2 is not None:
            val = R1 + R2
            steps = ["Формула: R = R₁ + R₂", f"R = {R1} + {R2} = {val:.2f} Ом"]
        else:
            raise ValueError("Для поиска R нужны R₁ и R₂")
        return {"R": f"{val:.2f} Ом"}, steps, explanation

    if target == 'R1':
        if R is not None and R2 is not None:
            val = R - R2
            steps = ["Из R = R₁ + R₂: R₁ = R - R₂", f"R₁ = {R} - {R2} = {val:.2f} Ом"]
        else:
            raise ValueError("Для поиска R₁ нужны R и R₂")
        return {"R1": f"{val:.2f} Ом"}, steps, explanation

    if target == 'R2':
        if R is not None and R1 is not None:
            val = R - R1
            steps = ["Из R = R₁ + R₂: R₂ = R - R₁", f"R₂ = {R} - {R1} = {val:.2f} Ом"]
        else:
            raise ValueError("Для поиска R₂ нужны R и R₁")
        return {"R2": f"{val:.2f} Ом"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['series'] = {
    "name": "Последовательное соединение",
    "category": "Электричество",
    "icon": "🔗",
    "image": "/static/img/series.svg",
    "quantities": {
        "R1": ("Сопротивление R₁", "Ом"),
        "R2": ("Сопротивление R₂", "Ом"),
        "R": ("Общее сопротивление R", "Ом"),
    },
    "targets": {
        "R": "Общее сопротивление R",
        "R1": "Сопротивление R₁",
        "R2": "Сопротивление R₂",
    },
    "solve": solve_series,
}


# ============================================================
# 12. Электричество: Параллельное соединение
# ============================================================
def solve_parallel(known, target):
    R1, R2, R = known.get('R1'), known.get('R2'), known.get('R')
    explanation = "Параллельное соединение: R = R₁·R₂ / (R₁ + R₂)."

    if target == 'R':
        if R1 is not None and R2 is not None and (R1 + R2) != 0:
            val = (R1 * R2) / (R1 + R2)
            steps = ["Формула: R = R₁·R₂ / (R₁ + R₂)", f"R = {R1}·{R2} / ({R1} + {R2}) = {val:.2f} Ом"]
        else:
            raise ValueError("Для поиска R нужны R₁ и R₂ (R₁+R₂ ≠ 0)")
        return {"R": f"{val:.2f} Ом"}, steps, explanation

    if target == 'R1':
        if R is not None and R2 is not None and (R2 - R) != 0:
            val = (R * R2) / (R2 - R)
            steps = ["Из R = R₁·R₂/(R₁+R₂): R₁ = R·R₂ / (R₂ - R)", f"R₁ = {R}·{R2} / ({R2} - {R}) = {val:.2f} Ом"]
        else:
            raise ValueError("Для поиска R₁ нужны R и R₂ (R₂ ≠ R)")
        return {"R1": f"{val:.2f} Ом"}, steps, explanation

    if target == 'R2':
        if R is not None and R1 is not None and (R1 - R) != 0:
            val = (R * R1) / (R1 - R)
            steps = ["Из R = R₁·R₂/(R₁+R₂): R₂ = R·R₁ / (R₁ - R)", f"R₂ = {R}·{R1} / ({R1} - {R}) = {val:.2f} Ом"]
        else:
            raise ValueError("Для поиска R₂ нужны R и R₁ (R₁ ≠ R)")
        return {"R2": f"{val:.2f} Ом"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['parallel'] = {
    "name": "Параллельное соединение",
    "category": "Электричество",
    "icon": "🔀",
    "image": "/static/img/parallel.svg",
    "quantities": {
        "R1": ("Сопротивление R₁", "Ом"),
        "R2": ("Сопротивление R₂", "Ом"),
        "R": ("Общее сопротивление R", "Ом"),
    },
    "targets": {
        "R": "Общее сопротивление R",
        "R1": "Сопротивление R₁",
        "R2": "Сопротивление R₂",
    },
    "solve": solve_parallel,
}


# ============================================================
# 13. Кинематика: Свободное падение
# ============================================================
def solve_freefall(known, target):
    t, h, v = known.get('t'), known.get('h'), known.get('v')
    g = 9.8
    explanation = "Свободное падение: h = g·t²/2, v = g·t."

    if target == 'h':
        if t is not None:
            val = g * t * t / 2
            steps = ["Формула: h = g·t²/2", f"h = 9.8·{t}²/2 = {val:.2f} м"]
        else:
            raise ValueError("Для поиска h нужно t")
        return {"h": f"{val:.2f} м"}, steps, explanation

    if target == 'v':
        if t is not None:
            val = g * t
            steps = ["Формула: v = g·t", f"v = 9.8·{t} = {val:.2f} м/с"]
        else:
            raise ValueError("Для поиска v нужно t")
        return {"v": f"{val:.2f} м/с"}, steps, explanation

    if target == 't':
        if h is not None and h >= 0:
            val = (2 * h / g) ** 0.5
            steps = ["Из h = g·t²/2: t = √(2h/g)", f"t = √(2·{h}/9.8) = {val:.2f} с"]
        elif v is not None and v >= 0:
            val = v / g
            steps = ["Из v = g·t: t = v/g", f"t = {v}/9.8 = {val:.2f} с"]
        else:
            raise ValueError("Для поиска t нужны h (h≥0) или v (v≥0)")
        return {"t": f"{val:.2f} с"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['freefall'] = {
    "name": "Свободное падение",
    "category": "Кинематика",
    "icon": "🍎",
    "image": "/static/img/freefall.svg",
    "quantities": {
        "t": ("Время t", "с"),
        "h": ("Высота h", "м"),
        "v": ("Скорость v", "м/с"),
    },
    "targets": {
        "h": "Высоту h",
        "v": "Скорость v",
        "t": "Время t",
    },
    "solve": solve_freefall,
}


# ============================================================
# 14. Кинематика: Баллистика (движение под углом к горизонту)
# ============================================================
def solve_ballistics(known, target):
    v0 = known.get('v0')
    alpha = known.get('alpha')
    t = known.get('t')

    # Перевод угла в радианы для математических функций
    import math
    alpha_rad = math.radians(alpha) if alpha is not None else None
    g = 9.8

    explanation = "Движение под углом к горизонту раскладывается на два независимых: равномерное по горизонтали и равноускоренное по вертикали."

    if target == 'L':
        if v0 is not None and alpha is not None:
            val = (v0 ** 2 * math.sin(2 * alpha_rad)) / g
            steps = ["Формула дальности: L = v₀²·sin(2α) / g", f"L = {v0}²·sin(2·{alpha}°) / 9.8 = {val:.2f} м"]
        else:
            raise ValueError("Для поиска L нужны v₀ и α")
        return {"L": f"{val:.2f} м"}, steps, explanation

    if target == 'H':
        if v0 is not None and alpha is not None:
            val = (v0 ** 2 * math.sin(alpha_rad) ** 2) / (2 * g)
            steps = ["Формула макс. высоты: H = v₀²·sin²(α) / (2g)",
                     f"H = {v0}²·sin²({alpha}°) / (2·9.8) = {val:.2f} м"]
        else:
            raise ValueError("Для поиска H нужны v₀ и α")
        return {"H": f"{val:.2f} м"}, steps, explanation

    if target == 't':
        if v0 is not None and alpha is not None:
            val = (2 * v0 * math.sin(alpha_rad)) / g
            steps = ["Формула времени полета: t = 2·v₀·sin(α) / g", f"t = 2·{v0}·sin({alpha}°) / 9.8 = {val:.2f} с"]
        else:
            raise ValueError("Для поиска t нужны v₀ и α")
        return {"t": f"{val:.2f} с"}, steps, explanation

    if target == 'v0':
        if alpha is not None and t is not None and math.sin(alpha_rad) != 0:
            val = (t * g) / (2 * math.sin(alpha_rad))
            steps = ["Из t = 2·v₀·sin(α)/g: v₀ = t·g / (2·sin(α))", f"v₀ = {t}·9.8 / (2·sin({alpha}°)) = {val:.2f} м/с"]
        elif alpha is not None and L is not None and math.sin(2 * alpha_rad) != 0:
            val = math.sqrt((L * g) / math.sin(2 * alpha_rad))
            steps = ["Из L = v₀²·sin(2α)/g: v₀ = √(L·g / sin(2α))",
                     f"v₀ = √({L}·9.8 / sin(2·{alpha}°)) = {val:.2f} м/с"]
        else:
            raise ValueError("Для поиска v₀ нужны (α, t) или (α, L)")
        return {"v0": f"{val:.2f} м/с"}, steps, explanation

    raise ValueError("Неизвестная цель")


TASKS['ballistics'] = {
    "name": "Баллистика (угол к горизонту)",
    "category": "Кинематика",
    "icon": "🎯",
    "image": "/static/img/ballistics.svg",
    "quantities": {
        "v0": ("Начальная скорость v₀", "м/с"),
        "alpha": ("Угол α", "градусы"),
        "t": ("Время полета t", "с"),
        "H": ("Макс. высота H", "м"),
        "L": ("Дальность L", "м"),
    },
    "targets": {
        "L": "Дальность L",
        "H": "Максимальную высоту H",
        "t": "Время полета t",
        "v0": "Начальную скорость v₀",
    },
    "solve": solve_ballistics,
}


# ============================================================
# 15. Термодинамика: Нагревание/Охлаждение (Q = c*m*ΔT)
# ============================================================
def solve_heat(known, target):
    c, m, dt, Q = known.get('c'), known.get('m'), known.get('dt'), known.get('Q')
    explanation = "Количество теплоты при нагревании: Q = c·m·ΔT, где c — удельная теплоемкость."

    if target == 'Q':
        if c is not None and m is not None and dt is not None:
            val = c * m * dt
            steps = ["Формула: Q = c·m·ΔT", f"Q = {c}·{m}·{dt} = {val:.2f} Дж"]
        else:
            raise ValueError("Для поиска Q нужны c, m и ΔT")
        return {"Q": f"{val:.2f} Дж"}, steps, explanation
    if target == 'm':
        if Q is not None and c is not None and dt is not None and (c * dt) != 0:
            val = Q / (c * dt)
            steps = ["Из Q = c·m·ΔT: m = Q / (c·ΔT)", f"m = {Q} / ({c}·{dt}) = {val:.2f} кг"]
        else:
            raise ValueError("Для поиска m нужны Q, c и ΔT")
        return {"m": f"{val:.2f} кг"}, steps, explanation
    raise ValueError("Неизвестная цель")


TASKS['heat'] = {
    "name": "Нагревание вещества",
    "category": "Термодинамика",
    "icon": "🔥",
    "image": "/static/img/heat.svg",
    "quantities": {
        "c": ("Удельная теплоемкость c", "Дж/(кг·°C)"),
        "m": ("Масса m", "кг"),
        "dt": ("Изменение температуры ΔT", "°C"),
        "Q": ("Количество теплоты Q", "Дж"),
    },
    "targets": {"Q": "Количество теплоты Q", "m": "Массу m"},
    "solve": solve_heat,
}


# ============================================================
# 16. Оптика: Закон отражения (угол падения = угол отражения)
# ============================================================
def solve_reflection(known, target):
    alpha, beta = known.get('alpha'), known.get('beta')
    explanation = "Закон отражения: угол падения равен углу отражения (α = β)."

    if target == 'beta':
        if alpha is not None:
            steps = ["Закон отражения: β = α", f"β = {alpha}°"]
            return {"beta": f"{alpha}°"}, steps, explanation
        else:
            raise ValueError("Для поиска β нужен угол падения α")
    if target == 'alpha':
        if beta is not None:
            steps = ["Закон отражения: α = β", f"α = {beta}°"]
            return {"alpha": f"{beta}°"}, steps, explanation
        else:
            raise ValueError("Для поиска α нужен угол отражения β")
    raise ValueError("Неизвестная цель")


TASKS['reflection'] = {
    "name": "Закон отражения света",
    "category": "Оптика",
    "icon": "🪞",
    "image": "/static/img/reflection.svg",
    "quantities": {
        "alpha": ("Угол падения α", "°"),
        "beta": ("Угол отражения β", "°"),
    },
    "targets": {"beta": "Угол отражения β", "alpha": "Угол падения α"},
    "solve": solve_reflection,
}