# 7. Безопасность

## 7.1 Аутентификация

### 7.1.1 Хэширование паролей

- **Алгоритм:** SHA-256
- **Соль:** 16 байт, случайная (`secrets.token_hex(16)`)
- **Формат хранения:** `salt:hash`

```python
def hash_password(password):
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}:{password_hash}"
```

### 7.1.2 Session-based аутентификация

- **Механизм:** Flask sessions (signed cookies)
- **Ключ сессии:** `app.secret_key`
- **Данные сессии:**
  - `user_id` — ID пользователя
  - `username` — имя пользователя

### 7.1.3 Защита от CSRF

- Flask-WTF не используется (простая архитектура)
- Session-токен привязан к cookie

## 7.2 Валидация входных данных

### 7.2.1 Формы

- **HTML5 валидация:** `required`, `type="number"`, `step="any"`
- **JavaScript валидация:** Проверка перед отправкой
- **Серверная валидация:** try/except в решателях

### 7.2.2 Числовые данные

```python
def to_float(key):
    val = data.get(key, '0')
    if not val or val.strip() == '':
        return 0.0
    return float(val)
```

### 7.2.3 Тригонометрические ограничения

- sin/cos: проверка диапазона [-1, 1]
- Углы: проверка диапазона (0, 90) для прямоугольного треугольника

## 7.3 Защита от XSS

- **Jinja2 autoescaping:** Включён по умолчанию
- **Escape всех переменных:** `{{ variable }}`
- **Безопасный рендеринг:** Нет `| safe` для пользовательских данных

## 7.4 SQL Injection

- **Параметризованные запросы:** Все запросы используют `?` placeholders
- **Нет конкатенации SQL:**

```python
# Безопасно
conn.execute("SELECT * FROM users WHERE username = ?", (username,))

# Опасно (НЕ ИСПОЛЬЗУЕТСЯ)
# conn.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

## 7.5 Защита сессии

### 7.5.1 Ограничения

- Сессия хранится в signed cookie
- Нет sensitive данных в session
- Session очищается при logout

### 7.5.2 Logout

```python
@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('index'))
```

## 7.6 Rate Limiting

- **Текущее состояние:** Не реализовано
- **Рекомендация:** Добавить Flask-Limiter для защиты от brute-force

## 7.7 Безопасность файлов

- **Static files:** Только из папки `static/`
- **Templates:** Только из папки `templates/`
- **Нет загрузки файлов:** Пользователи не могут загружать файлы

## 7.8 Секреты и конфигурация

### 7.8.1 Текущее состояние

```python
app.secret_key = 'physics-solver-secret-key-2025'
```

### 7.8.2 Рекомендации

- Использовать环境变量 для `secret_key`
- Не хардкодить секреты в коде
- Использовать `.env` файл

## 7.9 Чек-лист безопасности

| Проверка | Статус |
|----------|--------|
| XSS защита | ✅ Jinja2 autoescaping |
| SQL Injection | ✅ Параметризованные запросы |
| CSRF защита | ⚠️ Не реализовано |
| Rate Limiting | ⚠️ Не реализовано |
| Хэширование паролей | ✅ SHA-256 + salt |
| Валидация ввода | ✅ Серверная + клиентская |
| Secure cookies | ⚠️ Flask default |
| HTTPS | ⚠️ Зависит от deployment |

## 7.10 Рекомендации по улучшению

1. **Добавить Flask-Limiter** для защиты от brute-force
2. **Реализовать CSRF tokens** для всех форм
3. **Использовать bcrypt** вместо SHA-256 для паролей
4. **Настроить HTTPS** при deployment
5. **Добавить Secure cookie flags** (httponly, samesite)
6. **Реализовать 2FA** для повышенной безопасности
7. **Добавить логирование** подозрительных действий
