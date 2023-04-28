from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2
import numpy as np
import time
from flask_socketio import send, emit
import pyautogui
async_mode = None
from engineio.payload import Payload



Payload.max_decode_packets = 500
app = Flask(__name__)
socket_ = SocketIO(app, async_mode=async_mode, transport='udp')
change=0
def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
            images = pyautogui.screenshot()
            frame = np.array(images)
            try:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
              
            except Exception as e:
                    pass
       



@app.route('/')
def index():
    return render_template('index.html',
                           sync_mode=socket_.async_mode)
@app.route('/video_feed')
def video_feed():
   return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@socket_.on('my_event')
def test_message(message):
    print(message['data'])
@socket_.on('position')
def test_message(message):
    global change
    change=1
    pyautogui.move(message['data']['mouseX'],message['data']['mouseY'])
    print(message['data']['mouseX'],message['data']['mouseY'])
@socket_.on('clicked')
def test_message(message):
    pyautogui.click()
    print(message['data']['mouseX'],message['data']['mouseY'])
@socket_.on('keyboard')
def test_message(message):
    global change
    change=1
    pyautogui.press(message['data']['key'])
    print(message['data']['key'])

@socket_.on('connect')
def connect():
    print("Socket connection made")
if __name__ == '__main__':
    socket_.run(app, host='192.168.168.84',debug=True,port=5003)