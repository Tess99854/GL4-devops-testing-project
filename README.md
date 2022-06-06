# the-event

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
  ```
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
  ```
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
   ```
   {
	"type": "smart pass",
	"price": 99.00
   }
   ```
 - GET: /users:  (user authentication required)
 
   returns an array of users, each user object has its username and email
    ```
    http://localhost:8000/users
    ```
