import cv2
from flask_socketio import SocketIO, send, emit
import threading


def stream_camera(socketio):
    """
    Initializes the camera and starts a separate thread to continuously capture
    and emit frames over Socket.IO.
    """
    # Attempt to open the default camera (index 0)
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print('Error: Could not open camera.')
        return

    # Start a new thread running the 'emit_frames' function,
    # passing in the socketio instance and the camera object
    threading.Thread(target=emit_frames, args=(socketio, camera)).start()


def emit_frames(socketio, camera):
    """
    Continuously captures frames from the given camera, encodes them as JPEG,
    and emits them over the 'frame' event via Socket.IO.
    """
    while True:
        # Read a frame from the camera (returns a bool and the frame)
        _, frame = camera.read()

        # Resize the frame to (320 x 240) for smaller bandwidth usage
        frame = cv2.resize(frame, (320, 240))

        # Encode the image as JPEG at 40% quality to reduce size
        _, img_encoded = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 40])

        # Convert the encoded image to bytes
        img_bytes = img_encoded.tobytes()

        # Send the bytes over Socket.IO under the 'frame' event
        socketio.emit('frame', img_bytes)

        # Sleep briefly to avoid overwhelming the network
        # and to control frame rate (~30 FPS here)
        socketio.sleep(0.03)
