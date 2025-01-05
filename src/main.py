from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from streamer.Streamer import stream_camera
from gamepad.Gamepad import Gamepad
from program.Program import receive_message, start_program
import eventlet
from adxl345 import ADXL345
import threading

# Attempt to initialize the ADXL345 accelerometer
try:
    adxl345 = ADXL345()
except Exception as e:
    print(f"Error initializing ADXL345: {e}")
    adxl345 = None

# ---------------------------------------------------------
#                Flask and Socket.IO Setup
# ---------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# Configure CORS to allow any origin (*). Adjust for your needs in production.
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Socket.IO with eventlet as the async mode
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins='*')


# ---------------------------------------------------------
#             Acceleration Emission Function
# ---------------------------------------------------------
def send_acceleration():
    """
    Continuously retrieves acceleration data from the ADXL345
    and emits it via Socket.IO under the 'acceleration' event.
    Runs in its own thread.
    """
    while True:
        # If adxl345 is available, get axes data and emit
        if adxl345:
            socketio.emit('acceleration', adxl345.get_axes(True))
        # Sleep for 50 ms => ~20 updates/second
        socketio.sleep(0.05)


# ---------------------------------------------------------
#              Socket.IO Event Handlers
# ---------------------------------------------------------
@socketio.on('connect')
def handle_connect():
    """
    Called when a client connects. We start camera streaming
    and initialize program-specific setup if needed.
    """
    print('Client connected')
    try:
        # Start streaming frames from the camera
        stream_camera(socketio)
        # Run any GPIO / hardware program setup
        start_program()
    except Exception as e:
        print(f"Error in connect handler: {e}")


@socketio.on('disconnect')
def handle_disconnect():
    """
    Called when a client disconnects.
    """
    print('Client disconnected')


@socketio.on('gamepad')
def handle_message(msg):
    """
    Called when we receive a 'gamepad' event from the client.
    The message is JSON describing the gamepad state. We parse it,
    then pass the resulting Gamepad object to our business logic
    (receive_message).
    """
    # Convert JSON -> Gamepad instance
    gamepad = Gamepad.map_json_to_gamepad(msg)
    # Handle the gamepad inputs (e.g., to drive motors or steer)
    receive_message(gamepad)

    # Optionally retrieve ADXL345 data
    # (Here it's read but not used, or could be used for debugging)
    axes = adxl345.get_axes(True) if adxl345 else None


# ---------------------------------------------------------
#                  Application Entry Point
# ---------------------------------------------------------
if __name__ == '__main__':
    try:
        # Patch standard library to work with eventlet
        eventlet.monkey_patch()

        # Start a background thread to send acceleration data
        threading.Thread(target=send_acceleration, daemon=True).start()

        # Run the Socket.IO server, accessible on port 5000
        socketio.run(app, debug=True, port=5000, host='0.0.0.0')
    except Exception as e:
        print(f"Error starting the app: {e}")
