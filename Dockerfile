FROM python:3.12-slim

WORKDIR /librarysite

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY Pipfile Pipfile.lock ./
RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --system

# Copy application code
COPY librarysite/ ./librarysite/

# Copy and set up entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

WORKDIR /librarysite/librarysite

# Expose only the Django port
EXPOSE 8000

# Use entrypoint for setup tasks
ENTRYPOINT ["docker-entrypoint.sh"]

# Only start Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]