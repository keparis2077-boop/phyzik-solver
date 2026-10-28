import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / 'history.db'


def init_db():
    """Создаёт таблицу истории при первом запуске."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                task_name TEXT NOT NULL,
                inputs TEXT NOT NULL,
                results TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_solution(task_id, task_name, inputs, results):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO history (task_id, task_name, inputs, results, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (task_id, task_name, inputs, results, datetime.now().strftime('%d.%m.%Y %H:%M'))
        )


def get_history(limit=50):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM history ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def clear_history():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM history")