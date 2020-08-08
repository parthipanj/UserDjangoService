# User Management Microservice 
A Microservice to manage the user data in MySQL with Django REST framework

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/parthipanj/UserDjangoService.git
$ cd UserDjangoService
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000`.

## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(env)$ python manage.py test users
```

## Features

- User Application to manage the user details such as username, password, email, mobile number, and avatar. 
- Environment Variable Access
- Logging
- Custom Response Structure
- Custom Exception Handler
- Dockerfile and Docker stack file
- Test Cases (WIP) 


## Docker Deployment

Build a docker image using the Dockerfile 

```sh
$ docker build -t ${image_name}:${tag} .
$ docker image ls
```

Make sure you MySQL running in your system. If not deploy the MySQL service using this [stack](https://github.com/parthipanj/DockerStack/blob/master/mysql.yml) file.
Need to download and deploy it separately.

**Note: Make sure you have the mysql image in local. And change the MySQL image name, root password in the stack file as per your configuration**

```sh
$ docker stack deploy -c mysql.yml ${appname}
$ docker stack ls     # To check the stack is deployed 
$ docker service ls   # To check the MySQL service is created
$ docker container ls # To check the MySQL container is up and running
```

Deploy the User Microservice using the docker stack file.

**Note: Change the Django configurations and MySQL connections configuration in the `/config/env.yml` file.**

```sh
$ docker stack deploy -c docker-stack.yml ${appname}
$ docker stack ls     # To check the stack is deployed 
$ docker service ls   # To check the service is created
$ docker container ls # To check the container is up and running
```