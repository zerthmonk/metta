FROM node:10.15.3-alpine

WORKDIR /app
COPY ./front .
RUN npm install --save-dev

EXPOSE 8080
