FROM python:3.12-slim

WORKDIR /librarysite

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy --system

COPY librarysite/ ./librarysite/

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://github.com/mailhog/MailHog/releases/download/v1.0.1/MailHog_linux_amd64 -o /usr/local/bin/MailHog \
    && chmod +x /usr/local/bin/MailHog

WORKDIR /librarysite/librarysite

EXPOSE 8000 8025

CMD ["sh", "-c", "\
MailHog & \
python manage.py makemigrations && \
python manage.py migrate && \
echo \"from django.contrib.auth import get_user_model; User = get_user_model(); \
User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin','admin@example.com','adminpass')\" | python manage.py shell && \
python manage.py runserver 0.0.0.0:8000"]
