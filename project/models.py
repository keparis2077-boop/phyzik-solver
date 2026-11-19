import sqlite3
from datetime import datetime
from pathlib import Path
import secrets
import hashlib

DB_PATH = Path(__file__).parent / 'history.db'


def _get_connection():
    """Создаёт подключение к базе данных."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Инициализация таблиц пользователей и истории."""
    with _get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                avatar TEXT DEFAULT 'default',
                created_at TEXT NOT NULL,
                xp INTEGER DEFAULT 0,
                coins INTEGER DEFAULT 0,
                streak INTEGER DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_id TEXT NOT NULL,
                task_name TEXT NOT NULL,
                inputs TEXT NOT NULL,
                results TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        # Миграция: добавляем колонку user_id, если существует старая таблица с device_id
        try:
            conn.execute("ALTER TABLE history ADD COLUMN user_id INTEGER")
        except sqlite3.OperationalError:
            pass


def hash_password(password):
    """Хэширует пароль с помощью SHA-256 и случайной соли."""
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"


def check_password(password, password_hash):
    """Проверяет пароль, сравнивая с хэшем."""
    parts = password_hash.split(':')
    if len(parts) != 2:
        return False
    salt, stored_hash = parts
    computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return computed_hash == stored_hash


def register_user(username, email, password):
    """Регистрация нового пользователя. Возвращает (success, message, user_data)."""
    with _get_connection() as conn:
        try:
            password_hash = hash_password(password)
            created_at = datetime.now().strftime('%d.%m.%Y %H:%M')
            cursor = conn.execute(
                "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (username, email, password_hash, created_at)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return True, "Пользователь зарегистрирован", {
                'id': user_id,
                'username': username,
                'email': email,
                'avatar': 'default',
                'xp': 0,
                'coins': 0,
                'streak': 0
            }
        except sqlite3.IntegrityError:
            conn.row_factory = sqlite3.Row
            if conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone():
                return False, "Имя пользователя уже занято", None
            return False, "Email уже зарегистрирован", None


def login_user(username, password):
    """Вход пользователя. Возвращает user_data (dict) или None."""
    with _get_connection() as conn:
        conn.row_factory = sqlite3.Row
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if not user:
            return None
        if not check_password(password, user['password_hash']):
            return None
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'avatar': user['avatar'],
            'xp': user['xp'],
            'coins': user['coins'],
            'streak': user['streak']
        }


def get_user_by_id(user_id):
    """Получение данных пользователя по ID."""
    with _get_connection() as conn:
        conn.row_factory = sqlite3.Row
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user:
            return None
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'avatar': user['avatar'],
            'xp': user['xp'],
            'coins': user['coins'],
            'streak': user['streak'],
            'created_at': user['created_at']
        }


def save_solution(user_id, task_id, task_name, inputs, results):
    """Сохранение решения задачи в историю."""
    with _get_connection() as conn:
        created_at = datetime.now().strftime('%d.%m.%Y %H:%M')
        conn.execute(
            "INSERT INTO history (user_id, task_id, task_name, inputs, results, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, task_id, task_name, inputs, results, created_at)
        )
        conn.commit()


def get_history(user_id, limit=50):
    """Получение истории решений пользователя."""
    with _get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM history WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()
    return [dict(r) for r in rows]


def clear_history(user_id):
    """Очистка истории пользователя."""
    with _get_connection() as conn:
        conn.execute("DELETE FROM history WHERE user_id = ?", (user_id,))
        conn.commit()


def add_xp(user_id, amount):
    """Добавление опыта пользователю."""
    with _get_connection() as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (amount, user_id))
        conn.commit()
        user = conn.execute("SELECT xp FROM users WHERE id = ?", (user_id,)).fetchone()
        return user['xp']


def add_coins(user_id, amount):
    """Добавление монет пользователю."""
    with _get_connection() as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("UPDATE users SET coins = coins + ? WHERE id = ?", (amount, user_id))
        conn.commit()
        user = conn.execute("SELECT coins FROM users WHERE id = ?", (user_id,)).fetchone()
        return user['coins']
