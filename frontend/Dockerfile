FROM node:22-alpine AS build
WORKDIR /app

COPY package.json ./
RUN npm install --no-audit --no-fund

COPY index.html postcss.config.js tailwind.config.js tsconfig.json ./
COPY src ./src
ENV VITE_API_BASE_URL=/api/v1
RUN npm run build

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
