import sqlite3
from datetime import datetime
from pathlib import Path
import uuid
import os

DB_PATH = Path(__file__).parent / 'history.db'


def init_db():
    """Создаёт таблицу истории при первом запуске."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                task_id TEXT NOT NULL,
                task_name TEXT NOT NULL,
                inputs TEXT NOT NULL,
                results TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        # Добавляем колонку device_id, если таблицы уже существует
        try:
            conn.execute("ALTER TABLE history ADD COLUMN device_id TEXT")
        except sqlite3.OperationalError:
            pass  # колонка уже существует


def get_device_id(request):
    """Уникальный идентификатор устройства на основе IP + user-agent."""
    ip = request.remote_addr or 'unknown'
    ua = request.headers.get('User-Agent', '')[:100]
    # Создаём хеш из IP и user-agent для уникальности
    return f"{ip}_{ua[:50]}"


def save_solution(task_id, task_name, inputs, results, device_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO history (device_id, task_id, task_name, inputs, results, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (device_id, task_id, task_name, inputs, results, datetime.now().strftime('%d.%m.%Y %H:%M'))
        )


def get_history(device_id, limit=50):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM history WHERE device_id = ? ORDER BY id DESC LIMIT ?",
            (device_id, limit)
        ).fetchall()
    return [dict(r) for r in rows]


def clear_all_history():
    """Полная очистка истории при запуске."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM history")


def clear_device_history(device_id):
    """Очистка истории конкретного устройства."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM history WHERE device_id = ?", (device_id,))


def get_device_ids():
    """Получает список всех уникальных device_id."""
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT DISTINCT device_id FROM history ORDER BY device_id"
        ).fetchall()
    return [r['device_id'] for r in rows]
