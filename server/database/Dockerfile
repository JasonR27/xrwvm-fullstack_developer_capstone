FROM node:23-bullseye AS nodeapi

# Set the working directory for the API
WORKDIR /app

RUN npm install -g npm@9.1.3

ADD package.json .
ADD app.js .
ADD reviews.js .
ADD dealerships.js .
ADD data/dealerships.json .
ADD data/reviews.json .
ADD data/car_records.json .
COPY . .

RUN npm install

EXPOSE 3030

CMD [ "node", "app.js" ]
