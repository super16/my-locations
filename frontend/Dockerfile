FROM node:lts-alpine as frontend-build

WORKDIR /app
COPY package*.json ./
RUN npm i
COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=frontend-build /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf
