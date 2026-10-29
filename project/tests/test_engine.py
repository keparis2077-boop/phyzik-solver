"""
Тесты для engine.py — универсального решателя задач.
"""

import pytest
import math
from engine import (
    _eval_expression,
    _format_value,
    _fill_steps,
    _validate_constraints,
    solve_task,
    load_specs,
    validate_specs,
    PHYSICS_CONSTANTS,
)


# ─── Тесты _eval_expression ────────────────────────────────────


class TestEvalExpression:
    """Тесты функции вычисления выражений."""

    def test_simple_addition(self):
        assert _eval_expression("R1 + R2", {"R1": 3, "R2": 5}) == 8

    def test_simple_multiplication(self):
        assert _eval_expression("m * a", {"m": 5, "a": 2}) == 10

    def test_simple_division(self):
        assert _eval_expression("U / R", {"U": 10, "R": 2}) == 5.0

    def test_with_equals_sign(self):
        """Формулы вида 'F = m * a' должны работать."""
        assert _eval_expression("F = m * a", {"m": 3, "a": 4}) == 12

    def test_power(self):
        assert _eval_expression("v ** 2", {"v": 3}) == 9

    def test_complex_formula(self):
        """Кинематика: s = v0*t + a*t²/2"""
        result = _eval_expression("v0*t + a*t**2/2", {"v0": 10, "a": 2, "t": 5})
        assert result == pytest.approx(75.0)  # 10*5 + 2*25/2 = 50 + 25 = 75

    def test_with_math_functions(self):
        """Баллистика: sin, radians"""
        result = _eval_expression("sin(radians(alpha))", {"alpha": 30})
        assert result == pytest.approx(0.5, abs=0.001)

    def test_with_sqrt(self):
        result = _eval_expression("sqrt(2 * E / m)", {"E": 100, "m": 2})
        assert result == pytest.approx(10.0)

    def test_with_g_constant(self):
        """Константа g должна быть доступна."""
        result = _eval_expression("g * t", {"t": 5})
        assert result == pytest.approx(49.0)

    def test_division_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            _eval_expression("U / R", {"U": 10, "R": 0})


# ─── Тесты _format_value ──────────────────────────────────────


class TestFormatValue:
    """Тесты форматирования чисел."""

    def test_default_precision(self):
        assert _format_value(3.14159) == "3.142"

    def test_custom_precision(self):
        assert _format_value(3.14159, ".4f") == "3.1416"

    def test_integer_result(self):
        assert _format_value(10.0) == "10.000"

    def test_small_number(self):
        assert _format_value(0.001, ".4f") == "0.0010"


# ─── Тесты _fill_steps ────────────────────────────────────────


class TestFillSteps:
    """Тесты подстановки значений в шаги решения."""

    def test_simple_substitution(self):
        steps = ["v = {v0} + {a}·{t}"]
        result = _fill_steps(steps, {"v0": 10, "a": 2, "t": 5}, 20)
        assert result == ["v = 10 + 2·5"]

    def test_with_result_placeholder(self):
        steps = ["v = {v0} + {a}·{t} = {result:.3f} м/с"]
        result = _fill_steps(steps, {"v0": 10, "a": 2, "t": 5}, 20)
        assert result == ["v = 10 + 2·5 = 20.000 м/с"]

    def test_with_custom_precision(self):
        steps = ["F = {result:.2f} Н"]
        result = _fill_steps(steps, {}, 10.567)
        assert result == ["F = 10.57 Н"]

    def test_no_placeholder(self):
        steps = ["Формула: F = m·a"]
        result = _fill_steps(steps, {}, 10)
        assert result == ["Формула: F = m·a"]


# ─── Тесты _validate_constraints ──────────────────────────────


class TestValidateConstraints:
    """Тесты проверки ограничений."""

    def test_division_by_zero_constraint(self):
        constraints = [{"field": "t", "condition": "!=", "value": 0}]
        assert _validate_constraints(constraints, {"t": 0}) is not None
        assert _validate_constraints(constraints, {"t": 5}) is None

    def test_discriminant_validation(self):
        constraints = [{"expression": "v0**2 + 2*a*s", "condition": ">=", "value": 0}]
        assert _validate_constraints(constraints, {"v0": 1, "a": 2, "s": -10}) is not None
        assert _validate_constraints(constraints, {"v0": 1, "a": 2, "s": 10}) is None

    def test_r2_minus_r_constraint(self):
        constraints = [{"expression": "R2 - R", "condition": "!=", "value": 0}]
        assert _validate_constraints(constraints, {"R2": 5, "R": 5}) is not None
        assert _validate_constraints(constraints, {"R2": 5, "R": 3}) is None


# ─── Тесты solve_task ─────────────────────────────────────────


class TestSolveTask:
    """Тесты решения задач по спецификации."""

    def test_newton_second_law(self):
        """F = m * a"""
        template = {
            "variables": {
                "m": {"label": "Масса m", "unit": "кг"},
                "F": {"label": "Сила F", "unit": "Н"},
                "a": {"label": "Ускорение a", "unit": "м/с²"},
            },
            "solutions": [
                {
                    "target": "F",
                    "requires": ["m", "a"],
                    "formula": "F = m * a",
                    "steps": ["Формула: F = m·a", "F = {m}·{a} = {result:.3f} Н"],
                }
            ],
        }
        results, steps, explanation = solve_task(template, {"m": 5, "a": 2}, "F")
        assert results == {"F": "10.000 Н"}
        assert len(steps) == 2
        assert "10.000" in steps[1]

    def test_ohms_law_current(self):
        """I = U / R"""
        template = {
            "variables": {
                "U": {"label": "Напряжение U", "unit": "В"},
                "R": {"label": "Сопротивление R", "unit": "Ом"},
                "I": {"label": "Сила тока I", "unit": "А"},
            },
            "solutions": [
                {
                    "target": "I",
                    "requires": ["U", "R"],
                    "formula": "I = U / R",
                    "steps": ["I = {result:.3f} А"],
                }
            ],
        }
        results, steps, _ = solve_task(template, {"U": 10, "R": 2}, "I")
        assert results == {"I": "5.000 А"}

    def test_series_resistance(self):
        """R = R1 + R2"""
        template = {
            "variables": {
                "R1": {"label": "R₁", "unit": "Ом"},
                "R2": {"label": "R₂", "unit": "Ом"},
                "R": {"label": "R", "unit": "Ом"},
            },
            "solutions": [
                {
                    "target": "R",
                    "requires": ["R1", "R2"],
                    "formula": "R = R1 + R2",
                    "steps": ["R = {result:.3f} Ом"],
                }
            ],
        }
        results, _, _ = solve_task(template, {"R1": 3, "R2": 5}, "R")
        assert results == {"R": "8.000 Ом"}

    def test_parallel_resistance(self):
        """R = R1*R2 / (R1 + R2)"""
        template = {
            "variables": {
                "R1": {"label": "R₁", "unit": "Ом"},
                "R2": {"label": "R₂", "unit": "Ом"},
                "R": {"label": "R", "unit": "Ом"},
            },
            "solutions": [
                {
                    "target": "R",
                    "requires": ["R1", "R2"],
                    "formula": "R = R1 * R2 / (R1 + R2)",
                    "steps": ["R = {result:.3f} Ом"],
                }
            ],
        }
        results, _, _ = solve_task(template, {"R1": 6, "R2": 3}, "R")
        assert results == {"R": "2.000 Ом"}

    def test_kinematics_velocity(self):
        """v = v0 + a * t"""
        template = {
            "variables": {
                "v0": {"label": "v₀", "unit": "м/с"},
                "v": {"label": "v", "unit": "м/с"},
                "a": {"label": "a", "unit": "м/с²"},
                "t": {"label": "t", "unit": "с"},
            },
            "solutions": [
                {
                    "target": "v",
                    "requires": ["v0", "a", "t"],
                    "formula": "v = v0 + a * t",
                    "steps": ["v = {result:.3f} м/с"],
                }
            ],
        }
        results, _, _ = solve_task(template, {"v0": 10, "a": 2, "t": 5}, "v")
        assert results == {"v": "20.000 м/с"}

    def test_kinematics_distance(self):
        """s = v0*t + a*t²/2"""
        template = {
            "variables": {
                "v0": {"label": "v₀", "unit": "м/с"},
                "a": {"label": "a", "unit": "м/с²"},
                "t": {"label": "t", "unit": "с"},
                "s": {"label": "s", "unit": "м"},
            },
            "solutions": [
                {
                    "target": "s",
                    "requires": ["v0", "a", "t"],
                    "formula": "s = v0*t + a*t**2/2",
                    "steps": ["s = {result:.3f} м"],
                }
            ],
        }
        results, _, _ = solve_task(template, {"v0": 10, "a": 2, "t": 5}, "s")
        assert results == {"s": "75.000 м"}

    def test_free_fall_height(self):
        """h = g * t² / 2"""
        template = {
            "variables": {
                "t": {"label": "t", "unit": "с"},
                "h": {"label": "h", "unit": "м"},
            },
            "solutions": [
                {
                    "target": "h",
                    "requires": ["t"],
                    "formula": "g * t**2 / 2",
                    "steps": ["h = {result:.3f} м"],
                }
            ],
        }
        results, _, _ = solve_task(template, {"t": 3}, "h")
        assert results == {"h": "44.100 м"}

    def test_ballistics_range(self):
        """L = v0² * sin(2α) / g"""
        template = {
            "variables": {
                "v0": {"label": "v₀", "unit": "м/с"},
                "alpha": {"label": "α", "unit": "градусы"},
                "L": {"label": "L", "unit": "м"},
            },
            "solutions": [
                {
                    "target": "L",
                    "requires": ["v0", "alpha"],
                    "formula": "v0**2 * sin(2*radians(alpha)) / g",
                    "steps": ["L = {result:.3f} м"],
                }
            ],
        }
        results, _, _ = solve_task(template, {"v0": 20, "alpha": 45}, "L")
        # При α=45° sin(90°)=1, L = 400/9.8 ≈ 40.816
        assert results == {"L": "40.816 м"}

    def test_kinetic_energy(self):
        """E = m * v² / 2"""
        template = {
            "variables": {
                "m": {"label": "m", "unit": "кг"},
                "v": {"label": "v", "unit": "м/с"},
                "E": {"label": "E", "unit": "Дж"},
            },
            "solutions": [
                {
                    "target": "E",
                    "requires": ["m", "v"],
                    "formula": "m * v**2 / 2",
                    "steps": ["E = {result:.3f} Дж"],
                }
            ],
        }
        results, _, _ = solve_task(template, {"m": 2, "v": 3}, "E")
        assert results == {"E": "9.000 Дж"}

    def test_density(self):
        """ρ = m / V"""
        template = {
            "variables": {
                "m": {"label": "m", "unit": "кг"},
                "V": {"label": "V", "unit": "м³"},
                "rho": {"label": "ρ", "unit": "кг/м³"},
            },
            "solutions": [
                {
                    "target": "rho",
                    "requires": ["m", "V"],
                    "formula": "m / V",
                    "steps": ["ρ = {result:.3f} кг/м³"],
                }
            ],
        }
        results, _, _ = solve_task(template, {"m": 10, "V": 2}, "rho")
        assert results == {"rho": "5.000 кг/м³"}

    def test_archimedes_force(self):
        """F = ρ * g * V"""
        template = {
            "variables": {
                "rho": {"label": "ρ", "unit": "кг/м³"},
                "V": {"label": "V", "unit": "м³"},
                "F": {"label": "F", "unit": "Н"},
            },
            "solutions": [
                {
                    "target": "F",
                    "requires": ["rho", "V"],
                    "formula": "rho * g * V",
                    "steps": ["F = {result:.3f} Н"],
                }
            ],
        }
        results, _, _ = solve_task(template, {"rho": 1000, "V": 0.01}, "F")
        assert results == {"F": "98.000 Н"}

    def test_heat_quantity(self):
        """Q = c * m * ΔT"""
        template = {
            "variables": {
                "c": {"label": "c", "unit": "Дж/(кг·°C)"},
                "m": {"label": "m", "unit": "кг"},
                "dt": {"label": "ΔT", "unit": "°C"},
                "Q": {"label": "Q", "unit": "Дж"},
            },
            "solutions": [
                {
                    "target": "Q",
                    "requires": ["c", "m", "dt"],
                    "formula": "c * m * dt",
                    "steps": ["Q = {result:.3f} Дж"],
                }
            ],
        }
        results, _, _ = solve_task(template, {"c": 4200, "m": 1, "dt": 10}, "Q")
        assert results == {"Q": "42000.000 Дж"}

    def test_reflection_law(self):
        """β = α"""
        template = {
            "variables": {
                "alpha": {"label": "α", "unit": "°"},
                "beta": {"label": "β", "unit": "°"},
            },
            "solutions": [
                {
                    "target": "beta",
                    "requires": ["alpha"],
                    "formula": "alpha",
                    "steps": ["β = {alpha}°"],
                }
            ],
        }
        results, steps, _ = solve_task(template, {"alpha": 30}, "beta")
        assert results == {"beta": "30.000 °"}
        assert "30°" in steps[0]

    def test_missing_required_variable_raises(self):
        """Если не хватает переменных — ошибка."""
        template = {
            "variables": {"m": {"unit": "кг"}, "a": {"unit": "м/с²"}, "F": {"unit": "Н"}},
            "solutions": [
                {
                    "target": "F",
                    "requires": ["m", "a"],
                    "formula": "m * a",
                    "steps": [],
                }
            ],
        }
        with pytest.raises(ValueError, match="Не удалось найти решение"):
            solve_task(template, {"m": 5}, "F")

    def test_constraint_violation_raises(self):
        """Нарушение ограничения (деление на 0) должно вызвать ошибку."""
        template = {
            "variables": {"U": {"unit": "В"}, "R": {"unit": "Ом"}, "I": {"unit": "А"}},
            "solutions": [
                {
                    "target": "I",
                    "requires": ["U", "R"],
                    "formula": "U / R",
                    "steps": [],
                    "constraints": [{"field": "R", "condition": "!=", "value": 0}],
                }
            ],
        }
        with pytest.raises(ValueError):
            solve_task(template, {"U": 10, "R": 0}, "I")

    def test_validation_discriminant_raises(self):
        """Отрицательный дискриминант должен вызвать ошибку."""
        template = {
            "variables": {"v0": {"unit": "м/с"}, "a": {"unit": "м/с²"}, "s": {"unit": "м"}},
            "solutions": [
                {
                    "target": "t",
                    "requires": ["v0", "a", "s"],
                    "formula": "(-v0 + (v0**2 + 2*a*s)**0.5) / a",
                    "steps": [],
                    "validation": [
                        {
                            "expression": "v0**2 + 2*a*s",
                            "condition": ">=",
                            "value": 0,
                            "error": "Нет решения: подкоренное выражение отрицательно",
                        }
                    ],
                }
            ],
        }
        # v0=10, a=2, s=-100 => disc = 100 + 2*2*(-100) = 100 - 400 = -300 < 0
        with pytest.raises(ValueError):
            solve_task(template, {"v0": 10, "a": 2, "s": -100}, "t")


# ─── Тесты load_specs ─────────────────────────────────────────


class TestLoadSpecs:
    """Тесты загрузки спецификаций."""

    def test_load_all_specs(self):
        specs = load_specs()
        assert len(specs) == 16  # 16 задач в проекте

    def test_load_specific_category(self, tmp_path):
        """Загрузка из конкретной директории."""
        # Создаём тестовый YAML
        test_yaml = tmp_path / "test.yaml"
        test_yaml.write_text("""
templates:
  - id: test_task
    name: "Test"
    variables:
      x: {label: "x", unit: ""}
    solutions:
      - target: x
        requires: []
        formula: "x"
        steps: []
""", encoding="utf-8")

        specs = load_specs(tmp_path)
        assert "test_task" in specs
        assert specs["test_task"]["name"] == "Test"

    def test_load_specs_returns_dict(self):
        specs = load_specs()
        assert isinstance(specs, dict)

    def test_load_specs_keys_are_task_ids(self):
        specs = load_specs()
        for key in specs:
            assert isinstance(key, str)
            assert len(key) > 0


# ─── Тесты validate_specs ─────────────────────────────────────


class TestValidateSpecs:
    """Тесты валидации спецификаций."""

    def test_valid_specs_have_no_errors(self):
        errors = validate_specs()
        assert len(errors) == 0, f"Ошибки: {errors}"

    def test_detect_missing_id(self, tmp_path):
        """Обнаружение отсутствующего id."""
        test_yaml = tmp_path / "bad.yaml"
        test_yaml.write_text("""
templates:
  - name: "No ID"
    variables: {}
    solutions: []
""", encoding="utf-8")

        errors = validate_specs(tmp_path)
        assert any("нет id" in e for e in errors)

    def test_detect_missing_name(self, tmp_path):
        """Обнаружение отсутствующего name."""
        test_yaml = tmp_path / "bad.yaml"
        test_yaml.write_text("""
templates:
  - id: test
    variables: {}
    solutions: []
""", encoding="utf-8")

        errors = validate_specs(tmp_path)
        assert any("нет name" in e for e in errors)

    def test_detect_missing_variables(self, tmp_path):
        """Обнаружение отсутствующих variables."""
        test_yaml = tmp_path / "bad.yaml"
        test_yaml.write_text("""
templates:
  - id: test
    name: "Test"
    solutions: []
""", encoding="utf-8")

        errors = validate_specs(tmp_path)
        assert any("нет variables" in e for e in errors)

    def test_detect_missing_solutions(self, tmp_path):
        """Обнаружение отсутствующих solutions."""
        test_yaml = tmp_path / "bad.yaml"
        test_yaml.write_text("""
templates:
  - id: test
    name: "Test"
    variables:
      x: {label: "x", unit: ""}
""", encoding="utf-8")

        errors = validate_specs(tmp_path)
        assert any("нет solutions" in e for e in errors)

    def test_detect_duplicate_id(self, tmp_path):
        """Обнаружение дубликатов id."""
        test_yaml = tmp_path / "dup.yaml"
        test_yaml.write_text("""
templates:
  - id: dup_task
    name: "First"
    variables: {}
    solutions: []
  - id: dup_task
    name: "Second"
    variables: {}
    solutions: []
""", encoding="utf-8")

        errors = validate_specs(tmp_path)
        assert any("дубликат" in e for e in errors)

    def test_detect_missing_formula(self, tmp_path):
        """Обнаружение отсутствующей формулы."""
        test_yaml = tmp_path / "bad.yaml"
        test_yaml.write_text("""
templates:
  - id: test
    name: "Test"
    variables:
      x: {label: "x", unit: ""}
    solutions:
      - target: x
        requires: []
        steps: []
""", encoding="utf-8")

        errors = validate_specs(tmp_path)
        assert any("нет formula" in e for e in errors)

    def test_detect_missing_target(self, tmp_path):
        """Обнаружение отсутствующего target."""
        test_yaml = tmp_path / "bad.yaml"
        test_yaml.write_text("""
templates:
  - id: test
    name: "Test"
    variables:
      x: {label: "x", unit: ""}
    solutions:
      - requires: []
        formula: "x"
        steps: []
""", encoding="utf-8")

        errors = validate_specs(tmp_path)
        assert any("нет target" in e for e in errors)

    def test_detect_undeclared_variable(self, tmp_path):
        """Обнаружение необъявленной переменной в requires."""
        test_yaml = tmp_path / "bad.yaml"
        test_yaml.write_text("""
templates:
  - id: test
    name: "Test"
    variables:
      x: {label: "x", unit: ""}
    solutions:
      - id: sol1
        target: x
        requires: [y]
        formula: "y"
        steps: []
""", encoding="utf-8")

        errors = validate_specs(tmp_path)
        assert any("не объявлен" in e for e in errors)
