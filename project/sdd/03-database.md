# 3. База данных

## 3.1 Общая информация

- **Тип:** SQLite (file-based)
- **Файл:** `history.db`
- **Драйвер:** sqlite3 (встроенный в Python)
- **Шифрование:** SHA-256 с солью для паролей

## 3.2 Схема базы данных

### Таблица `users`

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | INTEGER | Уникальный идентификатор | PRIMARY KEY, AUTOINCREMENT |
| `username` | TEXT | Имя пользователя | UNIQUE, NOT NULL |
| `email` | TEXT | Email | UNIQUE, NOT NULL |
| `password_hash` | TEXT | Хэш пароля с солью | NOT NULL (format: `salt:hash`) |
| `avatar` | TEXT | Аватар пользователя | DEFAULT 'default' |
| `created_at` | TEXT | Дата регистрации | NOT NULL (format: `DD.MM.YYYY HH:MM`) |
| `xp` | INTEGER | Опыт пользователя | DEFAULT 0 |
| `coins` | INTEGER | Монеты пользователя | DEFAULT 0 |
| `streak` | INTEGER | Текущая серия | DEFAULT 0 |

### Таблица `history`

| Поле | Тип | Описание | Ограничения |
|------|-----|----------|-------------|
| `id` | INTEGER | Уникальный идентификатор | PRIMARY KEY, AUTOINCREMENT |
| `user_id` | INTEGER | ID пользователя | FOREIGN KEY → users(id), NOT NULL |
| `task_id` | TEXT | ID задачи | NOT NULL |
| `task_name` | TEXT | Название задачи | NOT NULL |
| `inputs` | TEXT | Входные данные | NOT NULL |
| `results` | TEXT | Результаты решения | NOT NULL |
| `created_at` | TEXT | Дата решения | NOT NULL (format: `DD.MM.YYYY HH:MM`) |

## 3.3 Индексы

```sql
-- Автоматически создаваемые SQLite
users.id (PRIMARY KEY)
users.username (UNIQUE)
users.email (UNIQUE)
history.id (PRIMARY KEY)
history.user_id (FOREIGN KEY)
```

## 3.4 Миграции

Система автоматически обрабатывает миграции:

1. **Проверка существования таблицы** — `CREATE TABLE IF NOT EXISTS`
2. **Добавление новых колонок** — `ALTER TABLE ADD COLUMN`
3. **Миграция device_id → user_id** — создание новой таблицы без устаревшего поля

## 3.5 Примеры запросов

### Регистрация пользователя
```sql
INSERT INTO users (username, email, password_hash, created_at)
VALUES (?, ?, ?, ?)
```

### Вход пользователя
```sql
SELECT * FROM users WHERE username = ?
```

### Сохранение решения
```sql
INSERT INTO history (user_id, task_id, task_name, inputs, results, created_at)
VALUES (?, ?, ?, ?, ?, ?)
```

### Получение истории
```sql
SELECT * FROM history WHERE user_id = ? ORDER BY id DESC LIMIT 50
```

### Обновление XP
```sql
UPDATE users SET xp = xp + ? WHERE id = ?
```

## 3.6 Безопасность данных

- Пароли хранятся в виде `salt:sha256(password + salt)`
- Соль генерируется случайно для каждого пользователя (`secrets.token_hex(16)`)
- Нет хранения паролей в открытом виде
- Session-based аутентификация (cookies)

## 3.7 Производительность

- **Оптимизация:** Индексы на PRIMARY KEY и UNIQUE полях
- **Лимиты:** История ограничена 50 записями за запрос
- **Кэширование:** Данные пользователей кэшируются в session

## 3.8 Резервное копирование

Файл `history.db` можно скопировать для бэкапа. SQLite поддерживает hot-backup API.
