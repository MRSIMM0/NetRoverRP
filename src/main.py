from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from streamer.Streamer import stream_camera
from gamepad.Gamepad import Gamepad
from program.Program import receive_message, start_program
import eventlet
from adxl345 import ADXL345
import threading
# Initialize ADXL345 accelerometer
try:
    adxl345 = ADXL345()
except Exception as e:
    print(f"Error initializing ADXL345: {e}")
    adxl345 = None

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')

def send_acceleration():
    while True:
        socketio.emit('acceleration', adxl345.get_axes(True))
        socketio.sleep(0.05)



@socketio.on('connect')
def handle_connect():
    print('Client connected')
    try:
        stream_camera(socketio)
        start_program()
    except Exception as e:
        print(f"Error in connect handler: {e}")

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('gamepad')
def handle_message(msg):
    gamepad = Gamepad.map_json_to_gamepad(msg)
    receive_message(gamepad)
    axes = adxl345.get_axes(True)

if __name__ == '__main__':
    try:
        eventlet.monkey_patch()
        threading.Thread(target=send_acceleration, daemon=True).start()
        socketio.run(app, debug=True, port=5000, host='0.0.0.0')
    except Exception as e:
        print(f"Error starting the app: {e}")