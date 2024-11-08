import cv2
from flask_socketio import SocketIO, send, emit
import threading

def stream_camera(socketio):
    camera = cv2.VideoCapture(3)
    if not camera.isOpened():
        print('Error: Could not open camera.')
        return
    threading.Thread(target=emit_frames, args=(socketio, camera)).start()

def emit_frames(socketio, camera):
    while True:
        _, frame = camera.read()
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()
        socketio.emit('frame', img_bytes)
        socketio.sleep(0.08)