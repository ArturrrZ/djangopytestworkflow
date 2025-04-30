FROM python:3.11-slim
WORKDIR /django
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1

# Команда запуска Gunicorn
CMD ["gunicorn", "djangopytest.wsgi:application", "--bind", "0.0.0.0:8000"]