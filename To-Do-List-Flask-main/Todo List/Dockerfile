# Используем легковесный базовый образ
FROM python:3.11-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Выполняем операции под root (по умолчанию в начале процесса)
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    build-base

# Копируем зависимости Python и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы приложения
COPY . .

# Создаём непривилегированного пользователя после установки зависимостей
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Изменяем права доступа для непривилегированного пользователя
RUN chown -R appuser:appgroup /app

# Переключаемся на непривилегированного пользователя
USER appuser

# Устанавливаем порт и переменные окружения
ENV FLASK_APP=app.py
EXPOSE 5001

# Запускаем приложение
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]