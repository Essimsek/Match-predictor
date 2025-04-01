FROM node:18-alpine

WORKDIR /app

# Use separate layer for production dependencies
RUN npm install -g http-server

# Install dependencies first for caching
COPY package*.json .
RUN npm install

# Copy source files
COPY . .

# Use this for development
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]