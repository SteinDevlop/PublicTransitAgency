# Etapa 1: Build de Flutter Web
FROM cirrusci/flutter:stable AS build
WORKDIR /app
COPY . .
RUN flutter build web

# Etapa 2: Servidor NGINX para servir la web
FROM nginx:alpine
COPY --from=build /app/build/web /usr/share/nginx/html
EXPOSE 80
