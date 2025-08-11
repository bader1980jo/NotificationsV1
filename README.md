# Notifications Service

A Django-based notification backend supporting email, SMS, push and in-app notifications.

## Features

- Modular design with Django apps and environment based settings.
- Supports multiple channels (email, SMS, push) with fallback logic.
- REST API secured with token authentication.
- Template management with dynamic placeholders and attachment support.
- Asynchronous and scheduled delivery using Celery.
- Firebase Cloud Messaging (FCM) integration example.
- Admin site for managing templates, devices and notification logs.

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Copy environment file and adjust values:

```bash
cp .env.example .env
```

3. Apply migrations and create a super user:

```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Start the development server and a Celery worker:

```bash
celery -A notification_service worker -l info
python manage.py runserver
```

5. Obtain an API token and send a notification:

```bash
# get token
curl -X POST -d "username=<user>&password=<pass>" http://localhost:8000/api/auth/token/

# send notification
curl -H "Authorization: Token <token>" \
     -H "Content-Type: application/json" \
     -d '{"template":1, "users":[1], "context":{"name":"World"}}' \
     http://localhost:8000/api/notifications/send/
```

## Docker (optional)

A basic Dockerfile can be created to containerize the application:

```bash
docker build -t notifications .
docker run --env-file .env -p 8000:8000 notifications
```

## Testing Strategy

Run unit tests with Django's test runner:

```bash
python manage.py test
```
For production projects consider adding integration tests and using tools like `pytest`, `factory_boy`, and `coverage` for more comprehensive suites.
