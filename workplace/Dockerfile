FROM node:19.7.0-alpine

ADD . /app

WORKDIR /app

COPY package*.json /app/

RUN npm install

CMD [ "npm", "start" ]