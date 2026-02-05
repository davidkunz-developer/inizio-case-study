# Použijeme oficiální Python image
FROM python:3.11-slim

# Nastavení pracovního adresáře
WORKDIR /app

# Nastavení proměnných prostředí
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalace závislostí
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopírování zdrojového kódu
COPY . .

# Exponování portu
EXPOSE 8000

# Spuštění aplikace
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
