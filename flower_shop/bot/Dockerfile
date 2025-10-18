FROM python:3.11-slim

WORKDIR /app

# Копируем requirements только для бота
COPY flower_shop/bot/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY flower_shop/bot/ .

# Запускаем бота
CMD ["python", "-u", "bot.py"]
