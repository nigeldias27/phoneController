from flask import Flask, render_template
from flask_socketio import SocketIO
import pyautogui
async_mode = None
app = Flask(__name__)
socket_ = SocketIO(app, async_mode=async_mode)
@app.route('/')
def index():
    return render_template('index.html',
                           sync_mode=socket_.async_mode)
@socket_.on('my_event')
def test_message(message):
    print(message['data'])
@socket_.on('position')
def test_message(message):
    pyautogui.move(message['data']['mouseX'],message['data']['mouseY'])
    print(message['data']['mouseX'],message['data']['mouseY'])
@socket_.on('clicked')
def test_message(message):
    pyautogui.click()
    print(message['data']['mouseX'],message['data']['mouseY'])
@socket_.on('keyboard')
def test_message(message):
    pyautogui.press(message['data']['key'])
    print(message['data']['key'])

@socket_.on('connect')
def connect():
    print("Socket connection made")
if __name__ == '__main__':
    socket_.run(app, debug=True,port=5002)