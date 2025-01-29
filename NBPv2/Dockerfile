# Użyj najnowszego obrazu Pythona 3.13
FROM python:3.13-slim

# Ustawienia środowiska
ENV PYTHONUNBUFFERED True

# Ustaw katalog roboczy
WORKDIR /app

# Kopiowanie plików projektu
COPY . .

# Zainstaluj wymagane pakiety systemowe
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalacja zależności Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Domyślna komenda uruchamiająca aplikację
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]