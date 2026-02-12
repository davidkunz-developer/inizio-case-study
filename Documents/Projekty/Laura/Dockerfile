FROM python:3.11-slim

WORKDIR /app

# Kopírování requirements a instalace závislostí
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopírování aplikace
COPY . .

# Exponování portu
EXPOSE 8021

# Spuštění aplikace
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8021"]
