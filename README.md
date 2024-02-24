This is a basic version of an interactive quiz bot that engages users in quizzes, evaluates their responses, and provides a final score based on their answers. In this we use Django channels websocket communication, redis as message broker, and Django sessions for temporary data storage.

Steps to run the project with Docker

Install Docker and Docker Compose (https://docs.docker.com/compose/install/)
Docker should be running
In the project root run docker-compose build and docker-compose up
Go to localhost to view the chatbot
Steps to run the project without Docker

Install required packages by running pip install -r requirements.txt
Install and run postgresql, and change the DATABASES config in settings.py, if required.
Install and run redis, and update the CHANNEL_LAYERS config in settings.py, if required.
In the project root run python manage.py runserver
Go to 127.0.0.1:8000 to view the chatbot
