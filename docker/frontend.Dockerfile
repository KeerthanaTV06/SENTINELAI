# Build stage
FROM node:20-alpine AS build
WORKDIR /app
COPY frontend/ ./
RUN rm -rf node_modules package-lock.json
RUN npm install
RUN npm run build

# Nginx to serve built assets
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
