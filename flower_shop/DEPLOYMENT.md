# 🚀 Деплой на Railway

## Быстрый деплой

### 1. Подготовка к деплою

Все файлы уже готовы:
- ✅ `Procfile` - команда запуска
- ✅ `requirements.txt` - зависимости Python
- ✅ `runtime.txt` - версия Python
- ✅ `Dockerfile` - для Docker деплоя

### 2. Деплой на Railway

1. **Создайте проект на Railway:**
   - Перейдите на [railway.app](https://railway.app)
   - Нажмите "New Project"
   - Выберите "Deploy from GitHub repo"
   - Подключите репозиторий `Djju69/Flowersbot`

2. **Добавьте PostgreSQL:**
   - В проекте нажмите "+ New"
   - Выберите "Database" → "PostgreSQL"

3. **Настройте переменные окружения:**
   ```
   BOT_TOKEN=your_bot_token_here
   ADMIN_CHAT_ID=your_admin_chat_id
   ADMIN_IDS=123456789,987654321
   WEBAPP_URL=https://your-domain.railway.app/webapp
   ```

4. **Деплой Mini App:**
   - Соберите Mini App: `npm run build`
   - Загрузите файлы из `webapp/dist/` на статический хостинг
   - Обновите `WEBAPP_URL` в переменных окружения

### 3. Проверка деплоя

После деплоя проверьте:
- ✅ Health check: `https://your-domain.railway.app/health`
- ✅ Webhook: `https://your-domain.railway.app/test-webhook`
- ✅ Bot отвечает на `/start`

## 🔧 Локальный запуск

```bash
# 1. Backend
cd flower_shop/backend
pip install -r requirements.txt
python seed_data.py
uvicorn main:app --reload

# 2. Mini App
cd flower_shop/webapp
npm install
npm run dev

# 3. Bot
cd flower_shop/bot
pip install -r requirements.txt
python bot.py
```

## 📱 Настройка Mini App

1. Соберите Mini App:
   ```bash
   cd flower_shop/webapp
   npm run build
   ```

2. Загрузите файлы из `dist/` на хостинг

3. Обновите `WEBAPP_URL` в переменных окружения бота

## 🎯 Готово!

Проект полностью готов к деплою и работе!
