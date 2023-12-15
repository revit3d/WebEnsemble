FROM node:21.4-slim
WORKDIR /app/

COPY package.json yarn.lock /app/

RUN yarn --no-dev
RUN yarn build