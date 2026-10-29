"""
Тесты для database.py — работы с базой данных истории.
"""

import pytest
import os
import tempfile
from pathlib import Path
from datetime import datetime

# Импортируем функции напрямую
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import init_db, save_solution, get_history, clear_history, DB_PATH


@pytest.fixture
def db_path(tmp_path):
    """Создаём временную БД для тестов."""
    test_db = tmp_path / "test_history.db"
    return test_db


@pytest.fixture(autouse=True)
def temp_db(db_path):
    """Используем временную БД для всех тестов."""
    global DB_PATH
    original_db_path = DB_PATH
    DB_PATH = db_path
    # Удаляем старую БД если есть
    if db_path.exists():
        db_path.unlink()
    init_db()
    yield
    DB_PATH = original_db_path
    # Очистка
    if db_path.exists():
        db_path.unlink()


class TestInitDb:
    """Тесты инициализации базы данных."""

    def test_creates_table(self):
        """init_db создаёт таблицу history."""
        global DB_PATH
        test_db = Path(tempfile.gettempdir()) / "test_init_db.db"
        original = DB_PATH
        DB_PATH = test_db
        if test_db.exists():
            test_db.unlink()
        init_db()
        # Проверяем через get_history, которая подключается к БД
        from database import get_history
        records = get_history()
        assert isinstance(records, list)
        DB_PATH = original
        if test_db.exists():
            test_db.unlink()

    def test_creates_table_if_not_exists(self):
        """Двойной вызов init_db не должен вызывать ошибку."""
        global DB_PATH
        test_db = Path(tempfile.gettempdir()) / "test_init_db2.db"
        original = DB_PATH
        DB_PATH = test_db
        if test_db.exists():
            test_db.unlink()
        init_db()
        init_db()  # не должно упасть
        from database import get_history
        records = get_history()
        assert isinstance(records, list)
        DB_PATH = original
        if test_db.exists():
            test_db.unlink()


class TestSaveSolution:
    """Тесты сохранения решения."""

    def test_save_solution(self):
        """Сохранение решения в БД."""
        save_solution("test_task", "Test Task", "x=1", "y=2")

        records = get_history()
        assert len(records) == 1
        assert records[0]["task_id"] == "test_task"
        assert records[0]["task_name"] == "Test Task"
        assert records[0]["inputs"] == "x=1"
        assert records[0]["results"] == "y=2"
        assert "created_at" in records[0]

    def test_save_multiple_solutions(self):
        """Сохранение нескольких решений."""
        clear_history()
        save_solution("task1", "Task 1", "a=1", "b=2")
        save_solution("task2", "Task 2", "c=3", "d=4")

        records = get_history()
        assert len(records) == 2

    def test_save_solution_with_special_chars(self):
        """Сохранение с русскими символами."""
        save_solution("задача", "Задача на русском", "v0=10", "v=20")

        records = get_history()
        assert records[0]["task_name"] == "Задача на русском"

    def test_save_solution_timestamp_format(self):
        """Проверка формата временной метки."""
        save_solution("task", "Task", "x=1", "y=2")
        records = get_history()

        # Формат: dd.mm.yyyy hh:mm
        timestamp = records[0]["created_at"]
        try:
            datetime.strptime(timestamp, "%d.%m.%Y %H:%M")
        except ValueError:
            pytest.fail(f"Неверный формат времени: {timestamp}")


class TestGetHistory:
    """Тесты получения истории."""

    def test_empty_history(self):
        """Пустая история возвращает пустой список."""
        clear_history()
        records = get_history()
        assert records == []

    def test_returns_list(self):
        records = get_history()
        assert isinstance(records, list)

    def test_returns_dicts(self):
        save_solution("task", "Task", "x=1", "y=2")
        records = get_history()
        assert isinstance(records[0], dict)

    def test_record_has_all_fields(self):
        save_solution("task_id_1", "Task Name", "input data", "result data")
        records = get_history()
        record = records[0]
        assert "id" in record
        assert "task_id" in record
        assert "task_name" in record
        assert "inputs" in record
        assert "results" in record
        assert "created_at" in record

    def test_limit_parameter(self):
        """Параметр limit ограничивает количество записей."""
        for i in range(10):
            save_solution(f"task_{i}", f"Task {i}", f"x={i}", f"y={i}")

        records = get_history(limit=5)
        assert len(records) == 5

    def test_order_is_descending(self):
        """Записи должны быть в обратном порядке (новые первыми)."""
        save_solution("task_1", "Task 1", "x=1", "y=1")
        import time
        time.sleep(0.01)
        save_solution("task_2", "Task 2", "x=2", "y=2")

        records = get_history()
        assert records[0]["task_id"] == "task_2"
        assert records[1]["task_id"] == "task_1"


class TestClearHistory:
    """Тесты очистки истории."""

    def test_clear_all_records(self):
        """clear_history удаляет все записи."""
        save_solution("task1", "Task 1", "x=1", "y=1")
        save_solution("task2", "Task 2", "x=2", "y=2")

        clear_history()
        records = get_history()
        assert records == []

    def test_clear_empty_history(self):
        """Очистка пустой истории не должна вызывать ошибку."""
        clear_history()  # не должно упасть

    def test_clear_is_persistent(self):
        """После очистки данные должны быть удалены."""
        save_solution("task", "Task", "x=1", "y=1")
        clear_history()

        # Переподключаемся и проверяем
        records = get_history()
        assert len(records) == 0
