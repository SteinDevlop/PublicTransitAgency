FROM node:24.1.0-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci --omit=dev --no-audit

COPY . .

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 8080
CMD ["node", "server.js"]