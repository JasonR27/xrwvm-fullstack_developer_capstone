# Use the official Node.js image for the API application
FROM node:19.0.0-slim AS api

# Set the working directory for the API
WORKDIR /app

RUN npm install -g npm@9.1.3

ADD package.json .
ADD app.js .
ADD reviews.js .
ADD dealerships.js .
ADD data/dealerships.json .
ADD data/reviews.json .
COPY . .
RUN npm install

EXPOSE 3030

CMD [ "node", "app.js" ]


# Use the official MongoDB image for the database
FROM mongo:latest AS database

# Copy entrypoint.sh
# COPY entrypoint.sh /app/entrypoint.sh

# # Fix line endings for entrypoint.sh
# RUN sed -i 's/\r$//' /app/entrypoint.sh

# RUN chmod +x /app/entrypoint.sh
# ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Set environment variables for MongoDB
# ENV MONGO_INITDB_ROOT_USERNAME=mongoadmin
# ENV MONGO_INITDB_ROOT_PASSWORD=secret

# COPY entrypointdb.sh /entrypointdb.sh

# Fix line endings for entrypoint.sh
# RUN sed -i 's/\r$//' /entrypointdb.sh


# run with necessary permissions
# RUN chmod +x /app/entrypointdb.sh
# ENTRYPOINT ["/bin/bash", "/entrypointdb.sh"]

# Expose the default MongoDB port
EXPOSE 27017

# Start MongoDB
CMD ["mongod"]


# Use the official mongo-express image as a base
FROM mongo-express AS mongo-express

# Copy the config.js file to the /config directory
COPY config.js config.js
COPY config.js /config.js
COPY config.js /config/config.js
COPY config.js /app/config.js

EXPOSE 8081
