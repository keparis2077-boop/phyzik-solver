"""
Тесты для loader.py — загрузчика спецификаций.
"""

import pytest
from loader import build_tasks_dict, group_by_category, TASKS


class TestBuildTasksDict:
    """Тесты функции build_tasks_dict."""

    def test_loads_all_tasks(self):
        tasks = build_tasks_dict()
        assert len(tasks) == 16

    def test_all_tasks_have_name(self):
        tasks = build_tasks_dict()
        for tid, t in tasks.items():
            assert "name" in t
            assert len(t["name"]) > 0

    def test_all_tasks_have_category(self):
        tasks = build_tasks_dict()
        for tid, t in tasks.items():
            assert "category" in t
            assert len(t["category"]) > 0

    def test_all_tasks_have_quantities(self):
        tasks = build_tasks_dict()
        for tid, t in tasks.items():
            assert "quantities" in t
            assert len(t["quantities"]) > 0

    def test_all_tasks_have_targets(self):
        tasks = build_tasks_dict()
        for tid, t in tasks.items():
            assert "targets" in t
            assert len(t["targets"]) > 0

    def test_all_tasks_have_solve_function(self):
        tasks = build_tasks_dict()
        for tid, t in tasks.items():
            assert callable(t["solve"])

    def test_all_tasks_have_icon(self):
        tasks = build_tasks_dict()
        for tid, t in tasks.items():
            assert "icon" in t

    def test_all_tasks_have_image(self):
        tasks = build_tasks_dict()
        for tid, t in tasks.items():
            assert "image" in t

    def test_task_ids_are_strings(self):
        tasks = build_tasks_dict()
        for tid in tasks:
            assert isinstance(tid, str)

    def test_specific_task_exists(self):
        """Проверяем наличие ключевых задач."""
        assert "newton" not in TASKS  # task_id из spec
        assert any("newton" in tid for tid in TASKS)
        assert any("ohm" in tid for tid in TASKS)
        assert any("kinematics" in tid or "uniform_acceleration" in tid for tid in TASKS)

    def test_quantities_structure(self):
        """Структура quantities: {key: (label, unit)}."""
        tasks = build_tasks_dict()
        # Находим задачу с quantities
        for tid, t in tasks.items():
            if t["quantities"]:
                for key, (label, unit) in t["quantities"].items():
                    assert isinstance(key, str)
                    assert isinstance(label, str)
                    assert isinstance(unit, str)
                break

    def test_solve_function_works(self):
        """Функция solve должна возвращать корректный результат."""
        tasks = build_tasks_dict()
        # Находим задачу Ньютона
        for tid, t in tasks.items():
            if "Ньютон" in t["name"]:
                results, steps, explanation = t["solve"]({"m": 5, "a": 2}, "F")
                assert "F" in results
                assert "10.000" in results["F"]
                assert len(steps) > 0
                break


class TestGroupByCategory:
    """Тесты группировки задач по категориям."""

    def test_returns_dict(self):
        groups = group_by_category()
        assert isinstance(groups, dict)

    def test_all_tasks_grouped(self):
        groups = group_by_category()
        total = sum(len(items) for items in groups.values())
        assert total == 16

    def test_has_expected_categories(self):
        groups = group_by_category()
        categories = list(groups.keys())
        assert "Кинематика" in categories
        assert "Динамика" in categories
        assert "Электричество" in categories
        assert "Энергия" in categories
        assert "Давление" in categories

    def test_each_task_in_one_category(self):
        groups = group_by_category()
        task_ids = []
        for items in groups.values():
            for tid, _ in items:
                task_ids.append(tid)
        assert len(task_ids) == len(set(task_ids))  # без дубликатов


class TestGlobalTasks:
    """Тесты глобальной переменной TASKS."""

    def test_tasks_is_dict(self):
        assert isinstance(TASKS, dict)

    def test_tasks_not_empty(self):
        assert len(TASKS) > 0

    def test_tasks_accessible(self):
        """TASKS должен быть доступен для импорта в app.py."""
        from loader import TASKS as imported_tasks
        assert imported_tasks is TASKS
