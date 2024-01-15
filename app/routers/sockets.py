from flask import Flask, request, session, Blueprint
from flask_socketio import join_room, leave_room, send, emit

from string import ascii_uppercase
import random

from ..extensions import socketio

sockets = Blueprint("sockets", __name__)

rooms = {}  # storing room asssignments
user_rooms = {} 

@socketio.on("join_room")
def enter_room(data):

    available_rooms = check_exisiting_rooms(rooms)

    name = data["username"]
    print("line 20: ", name)

    if not name:
        print("No Name")
        return

    if not available_rooms:
        room = generate_room_code(4)
        add_rooms(room)
    else:
        room = list(available_rooms.keys())[0]

    session["room"] = room
    session["name"] = name

    user_rooms[name] = room

    obj = {"room": room, "name": name, "success": True}

    ## replaced on the front-end

    print("available rooms: ", available_rooms)
    print("rooms: ", rooms)
    print("user_rooms: ", user_rooms)

    socketio.emit("receiveData", data=obj)
    socketio.emit("receiveRooms", data=rooms)
    socketio.emit("receivemoredata", data=user_rooms)
    handle_connect()

    return {"success": True, "room": room}


@socketio.on("sendRooms")
def receive(data):
    roomCode = data["r"]["room"]
    user = data["r"]["name"]

    print(rooms)
    # print(roomCode)
    # print(user)

    socketio.emit("receiveRooms2", data=rooms)


# @sockets.route("/gameroom")
# def game_room():
#     room = session.get("room")
#     name = session.get("name")
#     # if room is None or name is None or check_rooms(room):
#     if room is None or name is None:
#         ## replaced on the front-end
#         return redirect(url_for("sockets.home"))

#     ## replaced on the front-end
#     return render_template("game_room.html", room=room)


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
    rooms[room]["users"].append(name)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("leave_room")
def exit_room(data):
    room = data.get("room")
    leave_room(room)

@socketio.on("disconnect")
def handle_disconnect():
    room = session.get("room")
    name = session.get("name")

    if room in rooms:
        rooms[room]["members"] -= 1
        rooms[room]["users"].remove(name)
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
    rooms[data] = {"members": 0, "users": []}


def get_rooms():
    return rooms


def check_room_size(room):
    if rooms[room]["members"] >= 2:
        return True
    return False


def check_exisiting_rooms(rooms_R):
    available_rooms = {}  # storing available rooms
    for room in rooms_R:
        if not check_room_size(room):
            available_rooms[room] = rooms_R[
                room
            ]  ## adding the room to available if it does not have 2 players

    return available_rooms


@socketio.on("send_message")
def msg(data):
    sender_sid = request.sid

    room = data.get("room")
    name = data.get("username")
    user_rooms = data.get("user_rooms")
    user_room = user_rooms[name]

    if user_room in rooms:
        if name in rooms[user_room]["users"]:
            message = data.get("message")
            socketio.emit(
                "get_message", {"name": name, "message": message}, to=user_room
            )
            return

    print("Invalid room or user")

@socketio.on("send_user_rooms")
def get_user_rooms(data):
    room = data.get("room")
    name = data.get("username")
    user_rooms = data.get("user_rooms") or {}

    print("user_rooms: ", user_rooms)
    user_rooms[name] = room
    print("user_rooms: ", user_rooms)
    socketio.emit("sendback_user_rooms", data=user_rooms)
