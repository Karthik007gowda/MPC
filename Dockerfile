FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install packages directly
RUN pip install --no-cache-dir Flask==3.0.2 pandas==2.2.0 openpyxl==3.1.2 gunicorn==21.2.0

COPY . .

RUN mkdir -p uploads outputs

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "600", "app:app"]
