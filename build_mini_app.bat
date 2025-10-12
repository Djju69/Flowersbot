@echo off
REM Скрипт для сборки и подготовки Mini App к загрузке на Telegram hosting

echo 🚀 Сборка Mini App для Telegram hosting...

REM Переходим в папку webapp
cd webapp

REM Проверяем наличие package.json
if not exist "package.json" (
    echo ❌ Ошибка: package.json не найден в папке webapp
    pause
    exit /b 1
)

REM Устанавливаем зависимости
echo 📦 Установка зависимостей...
npm install

REM Проверяем переменные окружения
if not exist ".env.production" (
    echo ⚠️  Предупреждение: .env.production не найден
    echo Создайте файл .env.production с переменной VITE_API_URL
)

REM Собираем проект
echo 🔨 Сборка проекта...
npm run build

REM Проверяем успешность сборки
if not exist "dist" (
    echo ❌ Ошибка: папка dist не создана
    pause
    exit /b 1
)

echo ✅ Сборка завершена!
echo 📁 Папка dist готова для загрузки на Telegram hosting
echo.
echo 📋 Следующие шаги:
echo 1. Зайдите в @BotFather
echo 2. Выберите вашего бота
echo 3. Нажмите 'Mini App' → 'Upload Mini App'
echo 4. Загрузите содержимое папки dist
echo 5. Обновите WEBAPP_URL в Railway
echo.
echo 📂 Путь к файлам: %CD%\dist
pause
