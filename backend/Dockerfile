# ─── Base Image ──────────────────────────────────────────────────────────────
FROM python:3.12-slim

# ─── Variables de entorno de Python ──────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# ─── Directorio de trabajo ────────────────────────────────────────────────────
WORKDIR /app

# ─── Dependencias del sistema (Tesseract + ODBC Driver 17) ────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-spa \
    poppler-utils \
    curl \
    gnupg \
    unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list \
        > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ─── Dependencias de Python ───────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ─── Código de la aplicación ──────────────────────────────────────────────────
COPY . .

# ─── Puerto expuesto ─────────────────────────────────────────────────────────
EXPOSE 8000

# ─── Comando de inicio ────────────────────────────────────────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
