# Build frontend
FROM node:14 as frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Copy frontend build to Python environment
FROM python:3.12.0-slim-bookworm
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
ENV APP=/app
WORKDIR $APP

# Install the requirements
COPY requirements.txt $APP
RUN pip3 install -r requirements.txt

# Copy everything else
COPY . $APP

# Copy frontend build
COPY --from=frontend-build /frontend/build /app/frontend/public

EXPOSE 8000
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
