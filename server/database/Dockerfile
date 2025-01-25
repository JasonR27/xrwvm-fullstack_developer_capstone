# Use the official Node.js image for the API application
FROM node:19.0.0-slim AS api

# Set the working directory for the API
WORKDIR /app

RUN npm install -g npm@9.1.3

ADD package.json .
ADD app.js .
ADD review.js .
ADD dealership.js .
ADD data/dealerships.json .
ADD data/reviews.json .
COPY . .
RUN npm install

EXPOSE 3030

CMD [ "node", "app.js" ]


# Use the official MongoDB image for the database
FROM mongo:latest AS database

# Set environment variables for MongoDB
# ENV MONGO_INITDB_ROOT_USERNAME=mongoadmin
# ENV MONGO_INITDB_ROOT_PASSWORD=secret
# COPY entrypointdb.sh /entrypointdb.sh

# Fix line endings for entrypoint.sh
# RUN sed -i 's/\r$//' /entrypointdb.sh


# run with necessary permissions
# RUN chmod +x /app/entrypoint.sh
# ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]

# Expose the default MongoDB port
EXPOSE 27017

# Start MongoDB
CMD ["mongod"]


# Use the official mongo-express image as a base
FROM mongo-express AS mongo-express