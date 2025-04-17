FROM node:18-alpine

WORKDIR /app

RUN npm install -g http-server

COPY package*.json .
RUN npm install

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]