from flask import Flask, render_template
from flask_socketio import SocketIO
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
@socket_.on('connect')
def connect():
    print("Socket connection made")
if __name__ == '__main__':
    socket_.run(app, debug=True)