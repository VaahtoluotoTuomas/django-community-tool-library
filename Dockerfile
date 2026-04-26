FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY="dummy-key-for-build-process-only"
ENV DB_NAME="dummy"
ENV DB_USER="dummy"
ENV DB_PASSWORD="dummy"
ENV AZURE_STORAGE_CONNECTION_STRING="dummy"
ENV AZURE_STORAGE_ACCOUNT_NAME="dummy"

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "lainaamo_config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2"]