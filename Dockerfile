# Базовый образ
FROM python:3.10-slim

# Python настройки
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# PyTorch CPU
RUN pip install --no-cache-dir \
    torch==2.2.0+cpu \
    torchvision==0.17.0+cpu \
    -f https://download.pytorch.org/whl/torch_stable.html

# Зависимости проекта
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

# Nginx конфиг (если реально используешь nginx)
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Приложение
COPY pdd_app/ pdd_app/

# Модель
COPY melis_model.pth .

# Открываем порт
EXPOSE 8000

# Запуск FastAPI
CMD ["uvicorn", "pdd_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
