import atexit
from collections import Counter
from concurrent import futures
from io import BytesIO
import math, cmath
import os
import time

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from picamera import PiCamera
from socketIO_client import SocketIO

SPEED_MULTIPLIER = 200
UPDATES_PER_SECOND = 5
CAMERA_QUALITY = 10
CAMERA_FPS = 5

robot_ws_secret = os.getenv('ROBOT_WS_SECRET', '')

camera = PiCamera()
camera.resolution = (200, 300)
camera.framerate = CAMERA_FPS # 5

with BytesIO() as stream, SocketIO('https://crowd-controlled-robot.herokuapp.com', 443) as socketIO:
    # capture_continuous is an endless iterator. Using video port + low quality for speed.
    for _ in camera.capture_continuous(stream, format='jpeg', use_video_port=True, quality=CAMERA_QUALITY):
        stream.truncate()
        stream.seek(0)
        data = stream.read()
        print(type(data))
        print(type(bytearray(data)))
        socketIO.emit('robot_image_' + robot_ws_secret, data=bytearray(data))
        #socketIO.emit('robot_image_' + robot_ws_secret, bytearray(data, encoding="utf-8"))
        #socketIO.emit('robot_image_' + robot_ws_secret, data)
        stream.seek(0)
