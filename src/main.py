from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
from streamer.Streamer import stream_camera
import threading
from gamepad.Gamepad import Gamepad
from program.Program import receive_message, start_program
import eventlet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    stream_camera(socketio)
    start_program()

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('gamepad')
def handle_message(msg):
    gamepad = Gamepad.map_json_to_gamepad(msg)
    receive_message(gamepad)

if __name__ == '__main__':
    eventlet.monkey_patch()
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')
