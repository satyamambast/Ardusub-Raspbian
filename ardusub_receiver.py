import socket
import sys
import cv2
import pickle
import numpy as np
import struct 
import zlib

HOST=''
PORT=8485

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    #data = data[msg_size:]

    #frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    data = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame0 = data[0]
    frame1 = data[1]
    frame0 = cv2.imdecode(frame0, cv2.IMREAD_COLOR)
    frame1 = cv2.imdecode(frame1, cv2.IMREAD_COLOR)
    h0,w0 = frame0.shape[:2]
    h1,w1 = frame1.shape[:2]

    frame0=cv2.resize(frame0,(2*w0,2*h0), interpolation = cv2.INTER_LINEAR)
    frame1=cv2.resize(frame1,(2*w1,2*h1), interpolation = cv2.INTER_LINEAR)   

    cv2.imshow('ImageWindow0',frame0)
    cv2.imshow('ImageWindow1',frame1)
    cv2.waitKey(1)
