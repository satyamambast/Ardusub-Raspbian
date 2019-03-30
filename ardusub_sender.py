import cv2
import io
import socket
import struct
import time
import pickle

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.2.1', 5003))
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
    data0 = pickle.dumps(frame0, 1)
    data1 = pickle.dumps(frame1, 1)
    size0 = len(data0)
    size1 = len(data1)
    print("{}: {}".format(img_counter, size0))
    print("{}: {}".format(img_counter, size1))
    client_socket.sendall(struct.pack(">L", size0) + data0)
    client_socket.sendall(struct.pack(">L", size1) + data1)
    img_counter += 1

cam0.release()
cam1.release()
