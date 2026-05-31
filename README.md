# Todo App

Todo App is a comprehensive task and ticket management system built with Django and Django REST Framework. It provides a structured way for teams to manage tasks ("Quests") and handle support requests ("Tickets") within different departments. The application is containerized using Docker for easy setup and deployment.

## Features

-   **User and Department Management**: Organize users into specific departments.
-   **Role-Based Permissions**: Differentiates between standard users and superusers, with superusers having extended administrative privileges like creating users and quests.
-   **Task Management ("Quests")**:
    -   Create, assign, and track tasks with titles, descriptions, and deadlines.
    -   View tasks by user and date.
    -   Mark tasks as complete and add comments.
    -   History view to review all tasks and restore completed ones.
-   **Ticketing System**:
    -   Users can create tickets and assign them to a department.
    -   Department members can claim and work on tickets.
    -   Track ticket status (open, assigned, completed).
-   **RESTful API**: Exposes endpoints for managing Users, Departments, Quests, and Tickets.
-   **Dockerized Environment**: Easily set up the application and its PostgreSQL database using Docker Compose.

## Tech Stack

-   **Backend**: Python, Django, Django REST Framework
-   **Database**: PostgreSQL
-   **Frontend**: Django Templates, Bootstrap
-   **Containerization**: Docker, Docker Compose

## Getting Started

### Prerequisites

-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

### Installation and Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/radwan16/todoapp.git
    cd todoapp
    ```

2.  **Start the services using Docker Compose:**
    This command will build the Docker image for the web application and start the `web` and `db` services.
    ```sh
    docker-compose up --build -d
    ```

3.  **Apply database migrations:**
    ```sh
    docker-compose exec web python manage.py migrate
    ```

4.  **Create a superuser:**
    Follow the prompts to create an administrative user. You will need this to log in and manage the application.
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```
    *After creating the superuser, you'll need to create a `Department`, assign the superuser to it, and then you can start creating other users and assigning them to the same department.*

5.  **Access the application:**
    The application will be running and accessible at `http://localhost:8000`. Log in with your superuser credentials.

## Project Structure

```
.
├── Dockerfile              # Defines the container for the Django app
├── docker-compose.yml      # Orchestrates the web and database services
├── manage.py               # Django's command-line utility
├── requirements.txt        # Python dependencies
├── main/                   # Core app for Quests, Users, Departments
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── Tickets/                # App for the ticketing system
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
└── Todo/                   # Main Django project settings and configuration
    ├── settings.py
    └── urls.py
```

## API Endpoints

The application provides a REST API for programmatic access. You can obtain an authentication token by sending a POST request with user credentials to the `/api-token/` endpoint.

-   `/users/`: Manage users (requires authentication)
-   `/department/`: Manage departments
-   `/quest/`: Manage quests (tasks)
-   `/tickets/`: Manage tickets

### Example Usage:

**Get all quests:**
```http
GET /quest/
Authorization: Token YOUR_AUTH_TOKEN
```

**Create a new ticket:** 
```http
POST /tickets/
Authorization: Token YOUR_AUTH_TOKEN

{
    "title": "New Ticket Title",
    "description": "Detailed description of the issue.",
    "who": "username",
    "departament": 1
}
