# 🚀 Инструкция по деплою

## 📋 Обзор архитектуры

Проект состоит из трех компонентов:

1. **Backend API + Bot** → Railway
2. **Mini App** → Telegram Bot hosting
3. **PostgreSQL** → Railway

## 🚂 Деплой на Railway (Backend + Bot)

### 1. Создание проекта
1. Зайдите на [Railway](https://railway.app)
2. Создайте новый проект
3. Подключите GitHub репозиторий

### 2. Настройка PostgreSQL
1. Добавьте PostgreSQL сервис
2. Скопируйте `DATABASE_URL` из переменных окружения

### 3. Переменные окружения
```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Telegram Bot
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
ADMIN_CHAT_ID=123456789
ADMIN_IDS=123456789,987654321

# Webapp
WEBAPP_URL=https://your-webapp-url.com

# API
API_URL=https://your-app.railway.app

# Railway Configuration
PORT=8000
RAILWAY_ENVIRONMENT=production
RAILWAY_PUBLIC_DOMAIN=your-app.railway.app
WEBHOOK_URL=https://your-app.railway.app/webhook
```

### 4. Деплой
Railway автоматически задеплоит проект после подключения репозитория.

## 📱 Деплой Mini App на Telegram hosting

### 1. Сборка Mini App
```bash
cd webapp
npm install
npm run build
```

### 2. Настройка переменных окружения
Создайте файл `.env.production`:
```env
VITE_API_URL=https://your-app.railway.app
```

### 3. Пересборка с переменными
```bash
npm run build
```

### 4. Загрузка на Telegram hosting
1. Зайдите в [@BotFather](https://t.me/BotFather)
2. Выберите вашего бота
3. Нажмите "Mini App" → "Upload Mini App"
4. Загрузите папку `dist` из `webapp/`

### 5. Настройка URL
После загрузки Telegram предоставит URL вида:
```
https://t.me/your_bot/app
```

Обновите переменную `WEBAPP_URL` в Railway:
```env
WEBAPP_URL=https://t.me/your_bot/app
```

## 🔧 Локальная разработка

### 1. Установка зависимостей
```bash
# Backend + Bot
pip install -r requirements.txt

# Mini App
cd webapp
npm install
```

### 2. Настройка переменных
```bash
cp env.example .env
# Отредактируйте .env файл
```

### 3. Запуск через Docker Compose
```bash
docker-compose up -d
```

### 4. Или запуск отдельных компонентов
```bash
# Backend API
python main.py

# Telegram Bot
python bot.py

# Mini App
cd webapp
npm run dev
```

## 📊 Мониторинг

### Railway
- Логи доступны в панели Railway
- Health check: `https://your-app.railway.app/health`

### Vercel/Netlify
- Логи доступны в панели управления
- Аналитика трафика

## 🔒 Безопасность

### Переменные окружения
- Никогда не коммитьте `.env` файлы
- Используйте разные токены для dev/prod
- Регулярно обновляйте токены

### API
- Все endpoints защищены CORS
- Валидация входных данных
- Rate limiting для API

## 🐛 Отладка

### Backend API
```bash
# Проверка здоровья
curl https://your-app.railway.app/health

# Проверка товаров
curl https://your-app.railway.app/api/products
```

### Telegram Bot
- Проверьте webhook: `https://api.telegram.org/bot<TOKEN>/getWebhookInfo`
- Логи в Railway панели

### Mini App
- Проверьте консоль браузера
- Проверьте Network tab в DevTools

## 📈 Масштабирование

### Railway
- Автоматическое масштабирование
- Мониторинг ресурсов

### Vercel/Netlify
- CDN для статических файлов
- Автоматическое масштабирование

## 🔄 Обновления

### Backend + Bot
1. Закоммитьте изменения
2. Railway автоматически перезапустит

### Mini App
1. Внесите изменения в код
2. Пересоберите: `npm run build`
3. Загрузите новую версию на Telegram hosting

## ✅ Чеклист деплоя

- [ ] Railway проект создан
- [ ] PostgreSQL подключен
- [ ] Переменные окружения настроены
- [ ] Backend API работает
- [ ] Telegram Bot работает
- [ ] Mini App собран (`npm run build`)
- [ ] Mini App загружен на Telegram hosting
- [ ] Переменная `VITE_API_URL` настроена
- [ ] Переменная `WEBAPP_URL` обновлена
- [ ] Webhook настроен
- [ ] Тестовый заказ создан
- [ ] Уведомления работают

## 🆘 Поддержка

При проблемах с деплоем:
1. Проверьте логи в Railway/Vercel/Netlify
2. Проверьте переменные окружения
3. Проверьте подключение к базе данных
4. Проверьте webhook настройки

---

**Проект готов к продакшену!** 🚀
