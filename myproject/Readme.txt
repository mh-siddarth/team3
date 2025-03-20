Instructions to run the project
Create a virtual environment 
Install necessary packages
Run Redis Server using "redis-server"
Run a celery worker to perform scheduling using "celery -A project_name worker -l info"
Run a celery beat to schedule crontab using "celery -A project_name beat -l info"
Run the project using "py manage.py runserver"
