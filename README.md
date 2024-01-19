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
