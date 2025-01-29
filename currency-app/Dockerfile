# Używamy oficjalnego obrazu Node.js jako bazowego
FROM node:20 AS build

# Ustawienie katalogu roboczego w kontenerze
WORKDIR /app

# Kopiowanie pliku package.json i instalowanie zależności
COPY package.json package-lock.json ./
RUN npm install

# Kopiowanie wszystkich plików aplikacji do kontenera
COPY . .

# Budowanie aplikacji Angular
RUN npm run build --prod

# Instalowanie serwera HTTP do obsługi statycznych plików
RUN npm install -g http-server

# Uruchamianie serwera HTTP na porcie 4200
CMD ["http-server", "dist", "-p", "4200"]
