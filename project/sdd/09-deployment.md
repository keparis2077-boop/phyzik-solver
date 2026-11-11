# 9. Развёртывание

## 9.1 Локальная разработка

### 9.1.1 Требования

- Python 3.13+
- pip

### 9.1.2 Установка

```bash
# Клонирование репозитория
git clone <repository-url>
cd phyzik-solver/project

# Установка зависимостей
pip install -r requirements.txt

# Запуск
python app.py
```

### 9.1.3 URL

- **Локальный сервер:** http://localhost:5000
- **Адрес:** 0.0.0.0:5000

## 9.2 Production Deployment

### 9.2.1 Варианты хостинга

| Платформа | Описание | Стоимость |
|-----------|----------|-----------|
| **Heroku** | PaaS, easy deploy | Free tier available |
| **Railway** | PaaS, PostgreSQL support | Free tier available |
| **VPS (DigitalOcean)** | Полный контроль | от $5/мес |
| **Fly.io** | Edge deployment | Free tier available |
| **PythonAnywhere** | Простой Python хостинг | Free tier available |

### 9.2.2 Production Checklist

- [ ] Перенести `secret_key` в环境变量
- [ ] Настроить HTTPS (Let's Encrypt)
- [ ] Использовать gunicorn вместо flask dev server
- [ ] Настроить логирование
- [ ] Настроить бэкапы БД
- [ ] Добавить CORS если нужен API
- [ ] Настроить monitoring (Sentry, etc.)

## 9.3 Docker

### 9.3.1 Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### 9.3.2 docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    volumes:
      - ./data:/app/data
```

### 9.3.3 Сборка и запуск

```bash
# Сборка
docker-compose up --build

# Запуск в фоне
docker-compose up -d

# Логи
docker-compose logs -f
```

## 9.4 Nginx Configuration

```nginx
server {
    listen 80;
    server_name fizik.example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /app/static;
        expires 30d;
    }
}
```

## 9.5 Environment Variables

| Переменная | Описание | Пример |
|------------|----------|--------|
| `SECRET_KEY` | Ключ сессии | random string |
| `FLASK_ENV` | Режим работы | production |
| `DATABASE_URL` | Путь к БД | /app/data/history.db |
| `LOG_LEVEL` | Уровень логирования | INFO |

## 9.6 Monitoring

### 9.6.1 Recommended Tools

- **Sentry** — error tracking
- **Prometheus + Grafana** — metrics
- **Logstash** — log aggregation
- **Uptime Robot** — uptime monitoring

### 9.6.2 Metrics

- Количество активных пользователей
- Количество решённых задач
- Среднее время решения
- Ошибки решателей

## 9.7 Бэкапы

### 9.7.1 Автоматический бэкап

```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
cp history.db "$BACKUP_DIR/history_$DATE.db"
find $BACKUP_DIR -name "history_*.db" -mtime +30 -delete
```

### 9.7.2 Ручной бэкап

```bash
cp history.db history_backup_$(date +%Y%m%d).db
```

## 9.8 Обновление

### 9.8.1 Процесс деплоя

```bash
# 1. Pull latest changes
git pull origin main

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python -c "from models import init_db; init_db()"

# 4. Restart service
systemctl restart fizik-solver
```

### 9.8.2 Rollback

```bash
# Откат на предыдущую версию
git reset --hard HEAD~1
pip install -r requirements.txt
systemctl restart fizik-solver
```
