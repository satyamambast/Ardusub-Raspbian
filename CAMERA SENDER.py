import cv2
import io
import socket
import struct
import time
import pickle

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.2.1', 8888))
connection = client_socket.makefile('wb')
n=int(input("entercameraname"))
cam = cv2.VideoCapture(n)

cam.set(3, 320);
cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 1)
    size = len(data)


    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1

cam.release()
