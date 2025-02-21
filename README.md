# OFI Dashboard Backend

This is a Dockerized Django REST application that provides API endpoints to a front-end dashboard for process mining for the company OFI Services.

## Project Structure
ofi_dashboard_backend/ manage.py ofi_dashboard_backend/ __init__.py asgi.py settings.py urls.py wsgi.py



## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/ofi_dashboard_backend.git
    cd ofi_dashboard_backend
    ```

2. Build and run the Docker containers:

    ```sh
    docker-compose up --build
    ```

3. Apply database migrations:

    ```sh
    docker-compose run web python manage.py migrate
    ```

4. Create a superuser:

    ```sh
    docker-compose run web python manage.py createsuperuser
    ```

5. Access the application at [http://localhost:8000](http://localhost:8000).

## API Endpoints

The API endpoints will be documented here once they are implemented.

## Deployment

For deployment, follow the instructions provided by your hosting provider. Ensure that you set the `DJANGO_SETTINGS_MODULE` environment variable to `ofi_dashboard_backend.settings`.