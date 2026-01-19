# frontend/Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy dependency files first (for caching)
COPY package.json package-lock.json* ./

RUN npm install

# Copy the rest of the app
COPY . .

# Build Next.js
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]
