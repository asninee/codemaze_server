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
    userId = data["userId"]
    # print("line 20: ", name)

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
    session["user_id"] = userId

    user_rooms[name] = room

    obj = {"room": room, "name": name, "success": True}

    # print("available rooms: ", available_rooms)
    # print("rooms: ", rooms)
    # print("user_rooms: ", user_rooms)

    socketio.emit("receiveData", data=obj)
    socketio.emit("receiveRooms", data=rooms)
    socketio.emit("receivemoredata", data=user_rooms)
    handle_connect()

    return {"success": True, "room": room}


@socketio.on("sendRooms")
def receive(data):
    # print(rooms)
    socketio.emit("receiveRooms2", data=rooms)


@socketio.on("connect")
def handle_connect():
    room = session.get("room")
    name = session.get("name")
    id = session.get("user_id")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["users"].append(name)
    rooms[room]["user_ids"].append(id)
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
    id = session.get("user_id")

    if room in rooms:
        rooms[room]["members"] -= 1
        rooms[room]["users"].remove(name)
        rooms[room]["user_ids"].remove(id)
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



@socketio.on("setting_question")
def handle_set_question(data):
    room = session.get("room")
    rooms[room]["question_data"]["question"] = data.get("initialQ")
    rooms[room]["question_data"]["testcases"] = data.get("testCase")
    rooms[room]["question_data"]["expected"] = data.get("expectedOutcome")
    # print(rooms)


@socketio.on("getting_question")
def handle_get_question():
    room = session.get("room")
    question = rooms[room]["question_data"]
    socketio.emit("got_question", question, room=room)


# @socketio.on("send_message")
# def msg(data):
#     sender_sid = request.sid

#     room = data.get("room")
#     name = data.get("username")
#     user_rooms = data.get("user_rooms")
#     user_room = user_rooms[name]

#     if user_room in rooms:
#         if name in rooms[user_room]["users"]:
#             message = data.get("message")
#             socketio.emit(
#                 "get_message", {"name": name, "message": message}, to=user_room
#             )
#             return

# print("Invalid room or user")


def add_rooms(data):
    rooms[data] = {
        "members": 0,
        "users": [],
        "user_ids": [],
        "winner_id": 0,
        "question_data": {
            "question": "",
            "testcase": [],
        }
    }


@socketio.on("send_user_rooms")
def get_user_rooms(data):
    room = data.get("room")
    name = data.get("username")
    user_rooms = data.get("user_rooms") or {}
    #test
    # print("user_rooms: ", user_rooms)
    user_rooms[name] = room
    # print("user_rooms: ", user_rooms)
    socketio.emit("sendback_user_rooms", data=user_rooms)


@socketio.on("button_press")
def handle_button_press(data):
    room = session.get("room")
    # print(f"button pressed in room: {room}")
    socketio.emit("button_pressed", room=room)

@socketio.on("button_enable")
def handle_button_enable(data):
    room = session.get("room")
    # print(f"button enabled in room: {room}")
    socketio.emit("button_enabled", room=room)

@socketio.on("display_popup")
def handle_display_popup(data):
    room = session.get("room")
    # print(f"Popup displayed in room: {room}")
    socketio.emit("displayed_popup", room=room)

@socketio.on("hide_popup")
def handle_hide_popup(data):
    room = session.get("room")
    # print(f"Popup hidden in room: {room}")
    socketio.emit("hidden_popup", room=room)

@socketio.on("check_answer")
def handle_answer_state(data):
    room = session.get("room")
    trueORfalse = data
    print(f"current answer state: {trueORfalse}")
    socketio.emit("checked_answer", trueORfalse, room=room)


@socketio.on("set_opponent")
def handle_setting_userId(data):
    user_id = data
    room = session.get("room")
    room_user_ids = rooms[room]["user_ids"]
    for id in room_user_ids:
        if id != user_id:
            opponent_id = id

    socketio.emit("opponent_set", opponent_id, room=room)


@socketio.on("set_winner")
def handle_winner(data):
    room = session.get("room")
    winner_id = data
    socketio.emit("winner_set", winner_id, room=room)
