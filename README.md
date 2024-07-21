Project Description
The Task Management System is a web application designed to help users manage and track their tasks efficiently. 
It allows users to create, update, delete, and view tasks. The tasks can be categorized, prioritized, 
and their statuses can be tracked. This system is built with a focus on ease of use and provides
a robust set of features for task management.

Technologies Used
Backend:

Django
Django REST Framework
SQLite (default, can be configured to use other databases)

Frontend:

Django templates
HTML
CSS

Authentication:

Django authentication
dj-rest-auth (for REST API authentication)

Additional Libraries:

django-filter
django-cors-headers
Pillow (for image processing)
Installation and Setup
Prerequisites

Ensure you have the following installed:

Python 3.8+
pip (Python package installer)
Virtualvenv (optional, but recommended)
Step-by-Step Installation

1. Clone the repository:
https://github.com/LitoukaTanya/todolist.git

2. Create and activate a virtual environment (optional but recommended):
python -m venv venv
venv\Scripts\activate

3. Install the required dependencies:
pip install -r requirements.txt

4. Apply the database migrations:
python manage.py migrate

5.Create a superuser account:
python manage.py createsuperuser

Running the Application
1. Start the development server:
python manage.py runserver

2. Access the application in your web browser:
Open your browser and go to http://127.0.0.1:8000/

3. Admin interface:
To access the Django admin interface, go to http://127.0.0.1:8000/admin and log in with the superuser credentials you created earlier.

How to Run the Project

1. Follow the installation steps to set up the project environment.
2. Start the development server using python manage.py runserver.
3. Open your browser and navigate to http://127.0.0.1:8000/ to access the task management system.
4. Use the admin interface at http://127.0.0.1:8000/admin to manage users and other administrative tasks.

API Documentation
Base URL
http://127.0.0.1:8000/api/

Authentication
Most endpoints require authentication. Use the following endpoint to obtain a token:

Login
Endpoint: /api/dj-rest-auth/login/
Method: POST
Request:
{
  "username": "yourusername",
  "password": "yourpassword"
}
Response:
{
  "key": "yourauthtoken"
}
Include the token in the Authorization header for subsequent requests:
Authorization: Token yourauthtoken

Endpoints
Tasks
List all tasks

Endpoint: /api/task/listtask/
Method: GET
Response:

[
	{
			"id": 11,
			"title": "Read a Book",
			"description": "Read at least one chapter of a book",
			"status": "completed",
			"completed": true,
			"created_at": "2024-07-12T21:03:34.250502Z",
			"completed_at": "2024-07-21T21:29:07.178448Z",
			"updated_at": "2024-07-21T21:29:07.178448Z",
			"deleted_at": null,
			"deleted": false,
			"created_by": 5,
			"category": {
				"id": 3,
				"name": "Education",
				"description": "Tasks related to learning and educational activities",
				"created_at": "2024-07-10T07:33:29.676874Z",
				"updated_at": "2024-07-21T20:45:57.033252Z",
				"deleted_at": null,
				"deleted": false
			},
			"priority": {
				"id": 4,
				"name": "Low",
				"created_at": "2024-07-21T20:50:54.362306Z",
				"updated_at": "2024-07-21T20:50:54.362306Z",
				"deleted_at": null,
				"deleted": false
			},
			"status_display": "Completed"
		},
		...
]

Create a new task

Endpoint: /api/task/create/
Method: POST
Request:
{
    "title": "Football Practice",
    "description": "Practice football with the team",
    "status": "completed",
    "category": 5, 
    "priority": 2   
}
Response:
{
    "id": 25,
    "title": "Football Practice",
    "description": "Practice football with the team",
    "status": "completed",
    "completed": true,
    "created_at": "2024-07-21T22:10:43.043167Z",
    "completed_at": "2024-07-21T22:10:43.041167Z",
    "updated_at": "2024-07-21T22:10:43.043167Z",
    "deleted_at": null,
    "deleted": false,
    "created_by": 10,
    "category": 5,
    "priority": 2
}

Retrieve a task by ID

Endpoint: /api/task/<int:pk>/
Method: GET
Response:
{
    "id": 12,
    "title": "Morning Jogging",
    "description": "Go for a 30-minute jog in the park",
    "status": "pending",
    "completed": false,
    "created_at": "2024-07-12T21:05:09.137461Z",
    "completed_at": null,
    "updated_at": "2024-07-21T21:23:58.113334Z",
    "deleted_at": null,
    "deleted": false,
    "created_by": 10,
    "category": {
        "id": 5,
        "name": "Sport",
        "description": "Tasks related to sports activities",
        "created_at": "2024-07-12T21:03:07.567620Z",
        "updated_at": "2024-07-21T20:45:10.430053Z",
        "deleted_at": "2024-07-12T21:18:59Z",
        "deleted": false
    },
    "priority": {
        "id": 2,
        "name": "Medium",
        "created_at": "2024-07-08T16:25:48.920973Z",
        "updated_at": "2024-07-08T16:25:48.920973Z",
        "deleted_at": null,
        "deleted": false
    },
    "status_display": "Pending"
}

Update a task

Endpoint: /api/task/update/<int:pk>/
Method: PUT
Request:
{
    "id": 12,
    "title": "Morning Jogging",
    "description": "Go for a 30-minute jog in the park",
    "status": "pending",
    "completed": false,
    "created_at": "2024-07-12T21:05:09.137461Z",
    "completed_at": null,
    "updated_at": "2024-07-21T22:22:58.744375Z",
    "deleted_at": null,
    "deleted": false,
    "created_by": 10,
    "category": 5,
    "priority": 1
}
Response:
{
    "id": 12,
    "title": "Morning Jogging",
    "description": "Go for a 30-minute jog in the park",
    "status": "pending",
    "completed": false,
    "created_at": "2024-07-12T21:05:09.137461Z",
    "completed_at": null,
    "updated_at": "2024-07-21T22:22:58.744375Z",
    "deleted_at": null,
    "deleted": false,
    "created_by": 10,
    "category": 5,
    "priority": 1
}

Delete a task

Endpoint: /api/task/delete/<int:pk>/
Method: DELETE
Response: 204 No Content