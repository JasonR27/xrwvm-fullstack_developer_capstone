# Build frontend
FROM node:19.0.0-slim AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install -g npm@8.19.2
RUN npm install
COPY frontend/ ./
RUN npm run build

# Copy frontend build to a Python environment to serve it via the django app
# Use the official Python image as a parent image
FROM python:3.9-slim AS djangowebapp
ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1
ENV APP=/app
WORKDIR $APP


# Install GCC
RUN apt-get update && apt-get install -y gcc

# Install the requirements
COPY requirements.txt $APP
RUN pip install -U -r requirements.txt

# Copy everything else
COPY . $APP

# Copy frontend build
COPY --from=frontend-build /frontend/build /app/frontend/public

# Copy the nginx.conf file to the correct location
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Copy SSL certificates
COPY nginx/ssl /etc/nginx/ssl

# Copy entrypoint.sh
COPY entrypoint.sh /app/entrypoint.sh

# Fix line endings for entrypoint.sh
RUN sed -i 's/\r$//' /app/entrypoint.sh

# Copy the custom nginx configuration file
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Expose the app directly on the localhost address
EXPOSE 3000

RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"] 

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
