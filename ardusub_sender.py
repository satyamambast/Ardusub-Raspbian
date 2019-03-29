import cv2
import io
import socket
import struct
import time
import pickle

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.2.1', 8485))
connection = client_socket.makefile('wb')

cam0 = cv2.VideoCapture(0)
cam1 = cv2.VideoCapture(1)

cam0.set(3, 320);
cam1.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret0, frame0 = cam0.read()
    ret1, frame1 = cam1.read()
    result0, frame0 = cv2.imencode('.jpg', frame0, encode_param)
    result1, frame1 = cv2.imencode('.jpg', frame1, encode_param)
    d=[frame0,frame1]
    data = pickle.dumps(d, 1)
    size = len(data)


    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1

cam0.release()
cam1.release()
