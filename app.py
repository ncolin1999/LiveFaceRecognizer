from datetime import datetime
from os import posix_fadvise
from flask import Flask,render_template
from flask_socketio import SocketIO,send,emit
from werkzeug.serving import generate_adhoc_ssl_context
from recognizer import face_recognizer
import cv2
import sys
import random
import base64
app = Flask(__name__)
socket = SocketIO(app)


def convert_and_save(b64_string):
    name = ""
    
    with open("face.png", "wb") as fh:
        fh.write(base64.decodebytes(b64_string.encode()))
        img   = cv2.imread("face.png")
        rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        name = face_recognizer.recognize(rgb)
    return name



@app.route('/')
def home():
    return render_template('index.html')

@socket.on("message")
def on_message(msg):
    try:
        msg = convert_and_save(msg.split(',')[1])
        send(msg,broadcast = True)
    except Exception as e:
        print(e)



@socket.on("frame_received")
def frame_received(data):
    print(data)



if __name__ =='__main__':
    #app.run(debug=True,port=1223)
    socket.run(app,host="0.0.0.0",port=5001,ssl_context=('cert.pem', 'key.pem'))