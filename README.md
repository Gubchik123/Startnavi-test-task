<img title="Startnavi test task" alt="Header image" src="./header.png">

_API for managing posts and comments with AI moderation and auto-reply._

## Project modules

<a href='https://pypi.org/project/celery'><img alt='celery' src='https://img.shields.io/pypi/v/celery?label=celery&color=blue'></a> <a href='https://pypi.org/project/Django'><img alt='Django' src='https://img.shields.io/pypi/v/Django?label=Django&color=blue'></a> <a href='https://pypi.org/project/django-celery-beat'><img alt='django-celery-beat' src='https://img.shields.io/pypi/v/django-celery-beat?label=django-celery-beat&color=blue'></a> <a href='https://pypi.org/project/django-celery-results'><img alt='django-celery-results' src='https://img.shields.io/pypi/v/django-celery-results?label=django-celery-results&color=blue'></a> <a href='https://pypi.org/project/django-cors-headers'><img alt='django-cors-headers' src='https://img.shields.io/pypi/v/django-cors-headers?label=django-cors-headers&color=blue'></a> <a href='https://pypi.org/project/djangorestframework'><img alt='djangorestframework' src='https://img.shields.io/pypi/v/djangorestframework?label=djangorestframework&color=blue'></a> <a href='https://pypi.org/project/djoser'><img alt='djoser' src='https://img.shields.io/pypi/v/djoser?label=djoser&color=blue'></a> <a href='https://pypi.org/project/drf-spectacular'><img alt='drf-spectacular' src='https://img.shields.io/pypi/v/drf-spectacular?label=drf-spectacular&color=blue'></a> <a href='https://pypi.org/project/flower'><img alt='flower' src='https://img.shields.io/pypi/v/flower?label=flower&color=blue'></a> <a href='https://pypi.org/project/google_generativeai'><img alt='google_generativeai' src='https://img.shields.io/pypi/v/google_generativeai?label=google_generativeai&color=blue'></a> <a href='https://pypi.org/project/psycopg2-binary'><img alt='psycopg2-binary' src='https://img.shields.io/pypi/v/psycopg2-binary?label=psycopg2-binary&color=blue'></a> <a href='https://pypi.org/project/python-dotenv'><img alt='python-dotenv' src='https://img.shields.io/pypi/v/python-dotenv?label=python-dotenv&color=blue'></a> <a href='https://pypi.org/project/redis'><img alt='redis' src='https://img.shields.io/pypi/v/redis?label=redis&color=blue'></a> 

## Features

1. User registration;
2. User login;
3. API for managing posts;
4. API for managing comments;
5. Checking posts or comments at the time of creation for the presence of obscene language, insults, etc., and blocking such posts or comments.
6. Analytics on the number of comments that have been added to posts for a certain period. Example URL: /api/v1/posts/1/comments_analytics?date_from=2020-02-02&date_to=2022-02-15. The API returns analytics aggregated by days for each day, the number of comments created and the number of blocked comments.
7. The function of automatic reply to comments if the user has enabled it for his posts. The automatic response doesn't occur immediately, but after a period of time set by the user. Also, the answer relevant to the post and comment to which the answer is being made.

## Technology Stack

The project utilizes the following technologies and tools:

**Backend**:
- **Python** programming language (OOP);
- **Django** framework for building the application;
    - **Django REST Framework** for creating RESTful APIs;
    - **Djoser** for user authentication;
    - **Django CORS Headers** for handling Cross-Origin Resource Sharing (CORS);
    - **Django Celery Beat** for periodic tasks;
    - **Django Celery Results** for storing Celery task results;
    - **DRF Spectacular** for generating API documentation;
- **PostgreSQL** database (Django ORM);
- **Celery** for asynchronous task processing;
- **Redis** as a message broker for Celery;
- **Flower** for monitoring Celery tasks and workers;
- **Google GenerativeAI** for generating comments;
- **python-dotenv** for managing environment variables.

**Version Control**:
- **Git** for version control and collaboration.

## Environment Variables

To run this project, you will need to add the following environment variables:

`SECRET_KEY`
`DB_PORT` `DB_HOST` `DB_NAME` `DB_USER` `DB_PASSWORD`
`CENSORED_WORDS`
`GEMINI_API_KEY`

> Look at the .env.sample

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Gubchik123/Starnavi-test-task.git
    ```

2. Go to the project directory:

    ```bash
    cd Starnavi-test-task
    ```

### Without Docker (without Celery & Redis, without auto comment answers)

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database connection and configurations according to the selected database engine. Apply migrations
    ```bash
    python manage.py migrate
    ```

5. Run the Django development server:
    ```bash
    python manage.py runserver
    ```

    > **Note:** Don't forget about environment variables

6. Access the API Swagger documentation at:
    ```
    http://127.0.0.1:8000/api/schema/swagger/
    ```

### With Docker (with Celery & Redis, with auto comment answers)

3. Build the Docker image:
    ```bash
    docker-compose build
    ```

4. Run the Docker container:
    ```bash
    docker-compose up -d
    ```

5. Apply migrations:
    ```bash
    docker-compose run backend python manage.py migrate
    ```

6. Access the API Swagger documentation at:
    ```
    http://127.0.0.1:8000/api/schema/swagger/
    ```

### Testing

To run the tests, run the following command:

```bash
python manage.py test
```