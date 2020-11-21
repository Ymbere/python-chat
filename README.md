# Python Chat

## Introduction

The goal of this project is to create a simple using python socketio and rabbitmq.

## Features

-   UI for chat betten users
-   A bot to get stock prices with the command `/stock={stock name}`

## Installation

The app requires that you have a rabbitmq service running, you can install it on your machine or use docker. if you chose to use docker make sure you have it installed on your machine.

` docker run -d --hostname my-rabbit --name some-rabbit -p 8080:15672 -p 5672:5672 rabbitmq:3-management`

For the other steps of the instalation you can follow these steps:

-   Clone the project
-   Go the location where the project is located
-   `cd python-chat`
-   Create a virtual env `python3 -m virtualenv venv --python=python3`
-   Activate the virtual env `source venv/bin/activate`
-   Install de depencies for the project `pip install -r requirements.txt`\*

After this steps you have to start the services.

#### Back-End

-   cd python-chat
-   `source venv/bin/activate`
-   cd back-end
-   export export FLASK_APP=chat.py
-   flask run

#### Stock bot

-   cd python-chat
-   `source venv/bin/activate`
-   cd bot
-   python bot

#### Front-End

-   cd python-chat
-   `source venv/bin/activate`
-   cd front-end
-   python -m http.server 5500

:warning: Each service should be open in a new terminal window or inside a terminal multiplexer like tmux

### How to use

In your browser access `localhost:5500`, login with any username and password you want, the authentication is WIP.

## TODO:

-   Authentication for the user
-   Remove hard coded URLS
-   Create docker compose
-   Create chat rooms
-   Unit tests for the bot
