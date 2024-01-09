from flask import Flask, render_template, request, session, redirect, Blueprint
from flask_socketio import join_room, leave_room, send, SocketIO
from string import ascii_uppercase
import random

sockets= Blueprint("sockets", __name__)

@sockets.route("/home")
def hello():
    return "test123"
