# Build frontend
# FROM node:23-bullseye AS frontend-build
# WORKDIR /frontend
# COPY frontend/package*.json ./
# RUN npm install
# COPY frontend/ ./
# RUN npm run build

# Copy frontend build to Python environment
FROM python:3.12.0-slim-bookworm AS django_web_app
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
ENV APP=/app
WORKDIR $APP

# Install the requirements
COPY requirements.txt $APP
RUN pip3 install -r requirements.txt

# Copy entrypoint.sh
COPY entrypoint.sh /app/entrypoint.sh

# Copy dependency manager file
COPY manage.py /app/manage.py

# Fix line endings for entrypoint.sh
RUN sed -i 's/\r$//' /app/entrypoint.sh

# Copy everything else
# COPY . $APP
COPY ./djangoapp /app/djangoapp
COPY ./djangoproj /app/djangoproj
# COPY ./frontend /app/frontend
COPY ./static /app/static
COPY db.sqlite3 /app/db.sqlite3
# Copy frontend build
# COPY --from=frontend-build /frontend/build /app/frontend/public

EXPOSE 8000
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
