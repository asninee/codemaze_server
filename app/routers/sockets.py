from flask import Flask, render_template, request, session, redirect, Blueprint, url_for
from flask_socketio import join_room, leave_room, send

from string import ascii_uppercase
import random

from ..extensions import socketio

sockets= Blueprint("sockets", __name__)

rooms = {} #storing room asssignments


@sockets.route("/home", methods=["GET", "POST"])
def home():
    session.clear()
    available_rooms = check_exisiting_rooms(rooms)

    if request.method == "POST":
        name = request.form.get("name")
        print(name)
        join = request.form.get("join", False)

        if not name:
            print(name)
            return render_template("home.html", error="Enter a name", name=name)

        if join != False:
            if not available_rooms:
                room = generate_room_code(4)
                add_rooms(room)
            else:
                room = list(available_rooms.keys())[0]
            
        session["room"] = room
        session["name"] = name
        return redirect(url_for("sockets.game_room"))
    
    print(rooms)
    print(available_rooms)

    ## replaced on the front-end
    return render_template("home.html")

@sockets.route("/gameroom")
def game_room():
    room = session.get("room")
    name = session.get("name")
    # if room is None or name is None or check_rooms(room):
    if room is None or name is None:
        ## replaced on the front-end
        return redirect(url_for("sockets.home"))
    
    ## replaced on the front-end
    return render_template("game_room.html", room=room)

@socketio.on("connect")
def handle_connect():
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def handle_disconnect():
    room = session.get("room")
    name = session.get("name")

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} left room {room}")

def generate_room_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code

def add_rooms(data):
    rooms[data] = {"members": 0}


def check_room_size(room):
    if rooms[room]["members"] >= 2:
        return True
    return False

def get_rooms():
    return rooms

def check_exisiting_rooms(rooms_R):
    available_rooms = {} #storing available rooms
    for room in rooms_R:
        if not check_room_size(room):
            available_rooms[room] = rooms_R[room] ## adding the room to available if it does not have 2 players

    return available_rooms



    
# @socketio.on("message")
# def handle_message(msg):
#     print("Received message: " + msg)
#     socketio.emit("Message", msg, broadcast=True)
