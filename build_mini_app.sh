#!/bin/bash

# Скрипт для сборки и подготовки Mini App к загрузке на Telegram hosting

echo "🚀 Сборка Mini App для Telegram hosting..."

# Переходим в папку webapp
cd webapp

# Проверяем наличие package.json
if [ ! -f "package.json" ]; then
    echo "❌ Ошибка: package.json не найден в папке webapp"
    exit 1
fi

# Устанавливаем зависимости
echo "📦 Установка зависимостей..."
npm install

# Проверяем переменные окружения
if [ ! -f ".env.production" ]; then
    echo "⚠️  Предупреждение: .env.production не найден"
    echo "Создайте файл .env.production с переменной VITE_API_URL"
fi

# Собираем проект
echo "🔨 Сборка проекта..."
npm run build

# Проверяем успешность сборки
if [ ! -d "dist" ]; then
    echo "❌ Ошибка: папка dist не создана"
    exit 1
fi

echo "✅ Сборка завершена!"
echo "📁 Папка dist готова для загрузки на Telegram hosting"
echo ""
echo "📋 Следующие шаги:"
echo "1. Зайдите в @BotFather"
echo "2. Выберите вашего бота"
echo "3. Нажмите 'Mini App' → 'Upload Mini App'"
echo "4. Загрузите содержимое папки dist"
echo "5. Обновите WEBAPP_URL в Railway"
echo ""
echo "📂 Путь к файлам: $(pwd)/dist"
