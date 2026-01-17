FROM node:24-alpine
LABEL authors="Michał Gradzik"
RUN mkdir "frontend"
WORKDIR /frontend

COPY package*.json ./
#COPY node_modules ./node_modules
COPY . .
RUN npm ci

RUN npm install
RUN npm install -D vite


ENV HOST=0.0.0.0
EXPOSE 8000
ENV NODE_ENV=production
CMD [ "npm","run", "dev" ]