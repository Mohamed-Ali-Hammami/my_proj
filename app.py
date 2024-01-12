# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO
from fetch_info import websocket_handler
import asyncio
from flask_cors import CORS

app = Flask(__name__)
socket_io = SocketIO(app, cors_allowed_origins="*")
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

def background_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(websocket_handler(socket_io))

@socket_io.on('connect')
def handle_connect():
    print('Client connected')
    socket_io.start_background_task(target=background_task)

@socket_io.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == "__main__":
    socket_io.run(app, debug=True, use_reloader=False)

