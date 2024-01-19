# Codemaze API

The Codemaze API is a back-end server built using Python, Flask and Flask-RESTX that allows for auth operations on users (register, login, logout), and a multitude of user, problem and session operations. It also utilises Flask-SocketIO to generate and manage game session rooms.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Features](#features)
- [Screenshots](#screenshots)
- [Setup](#setup)
- [Configuration](#configuration)
- [Usage](#usage)

## Technologies Used

- [Python](https://www.python.org/) - version 3.12.1
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) - version 3.0.0
- [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/) - version 1.3.0
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/getting_started.html) - version 5.3.6

## Setup

Clone the repository and `cd` into the root repository directory:

```sh
git clone git@github.com:nine96as/reddy41_server.git && cd reddy41_server
```

Start up the virtual environment using `pipenv`:

```sh
pipenv shell
```

Install required dependencies:

```sh
pipenv install
```

> [!important]
> Please ensure you are using the Python version listed in the [Technologies Used](#technologies-used) section.

## Configuration

1. Fetch the `PROD_DB_URI` by creating a database instance, [using this guide](https://www.elephantsql.com/docs/index.html), where [ElephantSQL](https://www.elephantsql.com/) is used as the database provider

2. Fetch the `JWT_SECRET_KEY` by generating your own secret key [using this link](https://randomkeygen.com/)

3. Fetch the `OPENAI_API_KEY` [using this guide](https://www.windowscentral.com/software-apps/how-to-get-an-openai-api-key)

> [!warning]
> It is imperative that you do not ever share OpenAI API key with anybody, purposely or accidentally. If you accidentally commit your token, [revoke it immediately](https://platform.openai.com/account/api-keys) and generate a new one.

4. Create a `.env` file within the root repository directory, and fill it in as shown below:

```env
FLASK_RUN_PORT=4000
PROD_DB_URI=postgresql://...
JWT_SECRET_KEY=
OPENAI_API_KEY=
```

## Usage

Run the back-end API with:

```sh
flask run
```
=======
# Reddy41_Server - Codemaze
# 
This is the back end of our application containing the necessary files required for database setup, request routing, socket connections, and cross-web connection between users. To interact with our application please follow the instructions below! 

- NOTE: you need both client and server to be running to use the application

## Installation `and` Usage

- Set up client side: follow the instructions in the client repository (https://github.com/AleFin95/Reddy41_Client)
- Open your terminal and create a new folder:
    `mkdir [folder_name]`
- Inside that new folder run:
    `git clone https://github.com/nine96as/reddy41_server.git`
- After repo is cloned open with:
    `cd reddy41_server`
- Install required dependencies with:
    - `pip install pipenv`
    - `pipenv install` and `pipenv install --dev`
- Open project in code editor:
    `code .`
- Create a **.env** file inside your project:
- ![image](https://github.com/nine96as/reddy41_server/assets/146546964/cd6be723-23b4-4104-9f8c-4090b391ee49)
- To start run:
    `flask run` or `python run.py`

## Technologies
- Python
- Pytest 
- Flask
- Flask-socketio
- Flask_restx
- OpenAi
- SQLalchemy
- HTTP
- Werkzeug
- ElephantSQL

## Process
- Started by creating the projects file structure.
- Began by writing our __init__.py and run.py.
- Next added our models, extensions, and created seperate files for our different routers.
- Created templates to be used during development
- Wrote out starter functions, routes for our users, sockets, sessions, and problems.
- Built off of the preperation, writing more complex socket functions and routes.
- Removed templates, linking up to React front end.
- Ironed out functions, routes and socket connections.

## Wins `and` Challenges
### Wins
- Implemented Pytest coverage.
- Worked with and learned Flask, Flask_socketio, Flask_restx.
- Learned how to correctly use socket functions to communicate between front-end, back-end and users.
### Challenges
- Had to rewrite function logic to handle change from templates to front-end <-> back-end communication.
- Connecting two users and saving user info inside the same room.
- Creating routes to handle the different needs of the application.
- 
## Bugs
- Refresh during 1v1 game causes connection issues, unable to reconnect to same room.
- Data sent at the end of the game is only correct for the winner, not loser.
- Info is sent multiple times, should only be sent once per call.

## Future Features
- Improve data stored in rooms to allow for rounds to be played with multiple questions.
- Add socket events and different types of rooms for sending messages to one another.
- Add routes to get selected users profile data to display for other users who want to view another users profile.
- Larger room sizes.
