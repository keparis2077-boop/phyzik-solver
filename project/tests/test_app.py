"""
Тесты для Flask-приложения (app.py).
Тестируем маршруты через Flask test client.
"""

import pytest
import sys
from pathlib import Path

# Добавляем проект в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app, init_db


@pytest.fixture
def client():
    """Создаём тестового клиента Flask."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"

    with app.test_client() as client:
        # Инициализируем БД перед каждым тестом
        init_db()
        yield client


@pytest.fixture(autouse=True)
def clear_history(client):
    """Очищаем историю перед каждым тестом."""
    from database import clear_history
    clear_history()


class TestIndexPage:
    """Тесты главной страницы (/)."""

    def test_index_page_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_page_contains_title(self, client):
        response = client.get("/")
        assert b"\xd0\x92\xd1\x8b\xd0\xb1\xd0\xb5\xd1\x80\xd0\xb8\xd1\x82\xd0\xb5" in response.data

    def test_index_page_shows_total(self, client):
        response = client.get("/")
        assert b"16" in response.data  # 16 задач

    def test_index_page_contains_task_names(self, client):
        response = client.get("/")
        assert b"\xd0\x92\xd1\x82\xd0\xbe\xd1\x80\xd0\xbe\xd0\xb9" in response.data
        assert b"\xd0\x97\xd0\xb0\xd0\xba\xd0\xbe\xd0\xbd" in response.data
        assert b"\xd0\xa0\xd0\xb0\xd0\xb2\xd0\xbd\xd0\xbe\xd1\x83\xd1\x81\xd0\xba\xd0\xbe\xd1\x80\xd0\xb5\xd0\xbd\xd0\xbd\xd0\xbe\xd0\xb5" in response.data

    def test_index_page_contains_categories(self, client):
        response = client.get("/")
        assert b"\xd0\x9a\xd0\xb8\xd0\xbd\xd0\xb5\xd0\xbc\xd0\xb0\xd1\x82\xd0\xb8\xd0\xba\xd0\xb0" in response.data
        assert b"\xd0\x94\xd0\xb8\xd0\xbd\xd0\xb0\xd0\xbc\xd0\xb8\xd0\xba\xd0\xb0" in response.data
        assert b"\xd0\xad\xd0\xbb\xd0\xb5\xd0\xba\xd1\x82\xd1\x80\xd0\xb8\xd1\x87\xd0\xb5\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe" in response.data

    def test_index_page_has_task_links(self, client):
        response = client.get("/")
        # Проверяем, что есть ссылки на задачи
        assert b'/task/' in response.data


class TestTaskPage:
    """Тесты страницы задачи (/task/<task_id>)."""

    def test_valid_task_page(self, client):
        response = client.get("/task/uniform_acceleration")
        assert response.status_code == 200

    def test_invalid_task_redirects(self, client):
        response = client.get("/task/nonexistent_task")
        assert response.status_code == 302

    def test_task_page_contains_task_name(self, client):
        response = client.get("/task/uniform_acceleration")
        assert b"\xd0\xa0\xd0\xb0\xd0\xb2\xd0\xbd\xd0\xbe\xd1\x83\xd1\x81\xd0\xba\xd0\xbe\xd1\x80\xd0\xb5\xd0\xbd\xd0\xbd\xd0\xbe\xd0\xb5" in response.data

    def test_task_page_contains_form(self, client):
        response = client.get("/task/uniform_acceleration")
        assert b"<form" in response.data

    def test_task_page_contains_target_select(self, client):
        response = client.get("/task/uniform_acceleration")
        assert b'name="target"' in response.data

    def test_task_page_contains_input_fields(self, client):
        response = client.get("/task/uniform_acceleration")
        assert b'name="v0"' in response.data
        assert b'name="a"' in response.data


class TestSolvePage:
    """Тесты решения задачи (/solve/<task_id>)."""

    def test_solve_kinematics_success(self, client):
        """Успешное решение задачи кинематики."""
        response = client.post(
            "/solve/uniform_acceleration",
            data={
                "target": "v",
                "v0": "10",
                "a": "2",
                "t": "5",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"20.000" in response.data  # v = 10 + 2*5 = 20

    def test_solve_newton_success(self, client):
        """Успешное решение задачи Ньютона."""
        response = client.post(
            "/solve/newton_second_law",
            data={
                "target": "F",
                "m": "5",
                "a": "2",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"10.000" in response.data  # F = 5*2 = 10

    def test_solve_ohm_success(self, client):
        """Успешное решение закона Ома."""
        response = client.post(
            "/solve/ohms_law",
            data={
                "target": "I",
                "U": "10",
                "R": "2",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"5.000" in response.data  # I = 10/2 = 5

    def test_solve_series_resistance(self, client):
        """Решение последовательного соединения."""
        response = client.post(
            "/solve/series_resistance",
            data={
                "target": "R",
                "R1": "3",
                "R2": "5",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"8.00" in response.data  # R = 3 + 5 = 8

    def test_solve_parallel_resistance(self, client):
        """Решение параллельного соединения."""
        response = client.post(
            "/solve/parallel_resistance",
            data={
                "target": "R",
                "R1": "6",
                "R2": "3",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"2.00" in response.data  # R = 6*3/(6+3) = 2

    def test_solve_free_fall(self, client):
        """Свободное падение."""
        response = client.post(
            "/solve/free_fall",
            data={
                "target": "h",
                "t": "3",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"44.10" in response.data  # h = 9.8*9/2 = 44.1

    def test_solve_ballistics(self, client):
        """Баллистика."""
        response = client.post(
            "/solve/ballistics",
            data={
                "target": "L",
                "v0": "20",
                "alpha": "45",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"40.82" in response.data  # L = 400/9.8 ≈ 40.82

    def test_solve_density(self, client):
        """Плотность."""
        response = client.post(
            "/solve/density",
            data={
                "target": "rho",
                "m": "10",
                "V": "2",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"5.000" in response.data  # ρ = 10/2 = 5

    def test_solve_archimedes(self, client):
        """Сила Архимеда."""
        response = client.post(
            "/solve/archimedes_force",
            data={
                "target": "F",
                "rho": "1000",
                "V": "0.01",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"98.00" in response.data  # F = 1000*9.8*0.01 = 98

    def test_solve_heat(self, client):
        """Нагревание."""
        response = client.post(
            "/solve/heat_quantity",
            data={
                "target": "Q",
                "c": "4200",
                "m": "1",
                "dt": "10",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"42000.00" in response.data  # Q = 4200*1*10

    def test_solve_reflection(self, client):
        """Закон отражения."""
        response = client.post(
            "/solve/reflection_law",
            data={
                "target": "beta",
                "alpha": "30",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"30" in response.data

    def test_solve_missing_target_redirects(self, client):
        """Отсутствие target перенаправляет на задачу."""
        response = client.post(
            "/solve/uniform_acceleration",
            data={"v0": "10"},  # нет target
        )
        assert response.status_code == 302

    def test_solve_invalid_number_shows_error(self, client):
        """Некорректное число показывает ошибку."""
        response = client.post(
            "/solve/uniform_acceleration",
            data={
                "target": "v",
                "v0": "abc",
                "a": "2",
                "t": "5",
            },
        )
        assert response.status_code == 200
        assert b"\xd0\x9d\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd1\x80\xd0\xb5\xd0\xba\xd1\x82\xd0\xbd\xd0\xbe\xd0\xb5" in response.data

    def test_solve_nonexistent_task_redirects(self, client):
        """Несуществующая задача перенаправляет на главную."""
        response = client.post(
            "/solve/nonexistent_task",
            data={},
        )
        assert response.status_code == 302

    def test_solve_saves_to_history(self, client):
        """Решение сохраняется в историю."""
        from database import get_history

        client.post(
            "/solve/newton_second_law",
            data={"target": "F", "m": "5", "a": "2"},
        )

        records = get_history()
        assert len(records) == 1
        assert records[0]["task_id"] == "newton_second_law"

    def test_solve_shows_steps(self, client):
        """Результат содержит пошаговое решение."""
        response = client.post(
            "/solve/uniform_acceleration",
            data={
                "target": "v",
                "v0": "10",
                "a": "2",
                "t": "5",
            },
            follow_redirects=True,
        )
        # Проверяем, что есть шаги решения
        assert b"\xd0\xa5\xd0\xbe\xd0\xb4" in response.data


class TestHistoryPage:
    """Тесты страницы истории (/history)."""

    def test_history_page_returns_200(self, client):
        response = client.get("/history")
        assert response.status_code == 200

    def test_history_page_empty(self, client):
        """Пустая история."""
        response = client.get("/history")
        assert len(response.data) > 0

    def test_history_page_shows_solutions(self, client):
        """История показывает решения."""
        # Сохраняем решение
        client.post(
            "/solve/newton_second_law",
            data={"target": "F", "m": "5", "a": "2"},
        )

        response = client.get("/history")
        assert response.status_code == 200
        # Проверяем, что есть данные
        assert len(response.data) > 0


class TestHistoryClear:
    """Тесты очистки истории (/history/clear)."""

    def test_clear_history_redirects(self, client):
        response = client.post("/history/clear")
        assert response.status_code == 302

    def test_clear_history_works(self, client):
        # Сохраняем решение
        client.post(
            "/solve/newton_second_law",
            data={"target": "F", "m": "5", "a": "2"},
        )

        # Очищаем
        response = client.post("/history/clear", follow_redirects=True)
        assert response.status_code == 200


class TestReferencePage:
    """Тесты справочной страницы (/reference)."""

    def test_reference_page_returns_200(self, client):
        response = client.get("/reference")
        assert response.status_code == 200

    def test_reference_page_contains_constants(self, client):
        response = client.get("/reference")
        assert b"g" in response.data.lower() or b"\xd0\xa3\xd1\x81\xd0\xba\xd0\xbe\xd1\x80\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5" in response.data

    def test_reference_page_contains_formulas(self, client):
        response = client.get("/reference")
        assert b"F = m" in response.data


class TestNotFound:
    """Тесты обработки ошибок."""

    def test_nonexistent_page(self, client):
        response = client.get("/nonexistent")
        assert response.status_code == 404
