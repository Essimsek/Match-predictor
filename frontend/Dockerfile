FROM node:18-alpine

WORKDIR /app

# 1. Önce bağımlılıkları yükle (package.json değişmediyse cache kullanır)
COPY package*.json ./
RUN npm install

# 2. Tüm kaynak kodunu kopyala
COPY . .

# 3. Geliştirme sunucusunu başlat
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]


# 4. Portu aç (Vite varsayılanı 5173)
EXPOSE 5173