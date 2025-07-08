
# Simple Task API

A RESTful API built with Django REST Framework for managing tasks.

## Features

- CRUD operations for tasks (Create, Read, Update, Delete)
- RESTful endpoints with JSON responses
- Pagination for task lists
- Robust test coverage (TDD, edge cases)
- Clean code principles
- CI/CD with Jenkins (Linux & Windows pipelines)
- Virtual environment management

<<<<<<< HEAD
## Project Structure

```
simple_api/
  manage.py
  requirements.txt
  simple_api/
    settings.py
    urls.py
    ...
  tasks/
    domain/
      services.py
    infrastructure/
      models.py
    interface/
      serializers.py
      views.py
      urls.py
    migrations/
    tests.py
```
=======
- CI/CD Setup:
Jenkins pipeline configurations for both Windows and linux
- CI/CD github action added 
Automated testing, Django checks, and migrations
Virtual environment managemen
>>>>>>> 248c6306a36c3e4cbe9de65f0072d42c362b58a6

## Prerequisites

- Python 3.12+
- Django 5.1.4
- Django REST Framework

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the Server

```bash
python manage.py runserver
```

## Running Tests

```bash
pytest tasks/tests.py --cov=tasks --cov-report=term-missing -v
```

## CI/CD

- Jenkins pipelines for both Linux and Windows are provided in `.jenkins/`.
- Pipelines perform environment setup, Django checks, migrations, and run tests with coverage.

---

For more details, see the JenkinsFile in `.jenkins/` or reach out to the maintainer. 

