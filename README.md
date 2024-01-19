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
