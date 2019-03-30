import socket
import sys
import cv2
import pickle
import numpy as np
import struct 
import zlib

HOST='192.168.2.1'
PORT=5003

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data0 = b""
data1 = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    ######################DATA0######################################
    while len(data0) < payload_size:
        print("Recv: {}".format(len(data0)))
        data0 += conn.recv(4096)

    print("Done Recv: {}".format(len(data0)))
    packed_msg_size = data0[:payload_size]
    data0 = data0[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data0) < msg_size:
        data0 += conn.recv(4096)
    frame_data0 = data0[:msg_size]
    data0 = data0[msg_size:]

    frame0=pickle.loads(frame_data0, fix_imports=True, encoding="bytes")
    frame0 = cv2.imdecode(frame0, cv2.IMREAD_COLOR)
    h,w = frame0.shape[:2]

    frame0=cv2.resize(frame0,(2*w,2*h), interpolation = cv2.INTER_LINEAR)   
    
    cv2.imshow('ImageWindow',frame0)
    cv2.waitKey(1)
    ######################DATA1######################################
    while len(data1) < payload_size:
        print("Recv: {}".format(len(data1)))
        data1 += conn.recv(4096)

    print("Done Recv: {}".format(len(data1)))
    packed_msg_size = data1[:payload_size]
    data1 = data1[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data1) < msg_size:
        data1 += conn.recv(4096)
    frame_data1 = data1[:msg_size]
    data1 = data1[msg_size:]

    frame1=pickle.loads(frame_data1, fix_imports=True, encoding="bytes")
    frame1 = cv2.imdecode(frame1, cv2.IMREAD_COLOR)
    h,w = frame1.shape[:2]

    frame1=cv2.resize(frame0,(2*w,2*h), interpolation = cv2.INTER_LINEAR)   
    
    cv2.imshow('ImageWindow',frame1)
    cv2.waitKey(1)
