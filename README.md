# Devops/Testing Project

## Overview
This is a rest API built with Django, that includes Unit Testing, Integration testing and end-to-end testing as well as a CI/CD pipeline.
The fellowing REAMDE page will cover the following sections: 
- [Documentation](#documentation)
- [CI/CD pipeline](#cicd-pipeline)
- [Testing](#testing) 

## Documentation

To start the API make sure you have python and pip installed 

1. install the requirements by running the following command:
```
$ pip install -r requirements.txt
```
2. start the server by running: 
```
$ python manage.py runserver 
```
the service will be started on http://localhost:8000 , you can access the different endpoints throught this url.

### Available Endpoints

- POST: /register:
  ```
  http://localhost:8000/register 
  ```
  the body is a json object containing the username, email and password. Check this example: 
  ```json
  {
    "username": "john",
    "email": "john@email.com",
    "password": "bestPasswordEver"
  }
  ```
- POST: /login: 
  ```
  http://localhost:8000/login 
  ```
  the body is a json object containing the username, and password (it is possible to login using the email by passing the email in the username field)
  ```json
  {
    "username": "john@email.com",
    "password": "bestPasswordEver"
  }
  ```
  the response will contain an access token that can be used to authenticate the users later when added to the request headers.
  
 - GET: /tickets:  (no authentication required)
 
   returns an array of tickets, each ticket object has its type and price 
    ```
    http://localhost:8000/tickets
    ```
 - POST: /add_ticket:  (user authentication required)
   ```
   http://localhost:8000/add_ticket
   ```
   
   the body is a json object containing the type and price of the ticket. Check this example: 
   ```json
   {
	"type": "smartpass",
	"price": 99.00,
	"available_tickets": 100
   }
   ```
 - GET: /users:  (user authentication required)
 
   returns an array of users, each user object has its username and email
    ```
    http://localhost:8000/users
    ```
 - GET: /buy_ticket:  (user authentication required)
 
   Receives the type of ticket to be bought as a query param and reserves a ticket for the user if the specified type of tickets is still available.
    ```
    http://localhost:8000/buy_ticket?ticket_type=smartpass
    ```
    
## CI/CD Pipeline
Worked on the dockerization of the API using the following Dockerfile: 
```dockerfile
FROM python:3-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip 
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

The `venv` folder containing our dependencies should be added to the .dockerignore file.
To publish the docker image to docker hub every time we push new changes, a github action was created.

## Testing
The test files can be found under the folder `test`, this folder contains two types of tests:
### Unit tests:
- Testing the `manage_tickets`function: this function is responsible of assigning a ticket to the user and decreasing the number of available tickets, if no tickets are available it should return None.
- Testing the `buy_tickets` view: testing this view covers the following cases:
  - if `ticket_type` is not provided return a 400_bad_request code 
  - if `ticket_type` is provided and the `ticket_type` does not exist in the db return a 404_not_found code 
  - if `ticket_type` is provided, exists in the db but there are no more tickets available return a 404_not_found code
  - if `ticket_type` is provided, exists in the db and tickets are available return a 200_success code
