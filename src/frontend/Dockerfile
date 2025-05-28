FROM fluttercommunity/flutter:3.22.0 AS build
WORKDIR /app
COPY . .
RUN flutter build web

FROM nginx:alpine
COPY --from=build /app/build/web /usr/share/nginx/html
EXPOSE 80
