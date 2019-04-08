import cv2
import io
import socket
import struct
import time
import pickle
class MultiCam:
	def __init__(self,frame1,frame2):
		self.frame1=frame1
		self.frame2=frame2
	def displayallfeeds(self):
		cv2.imshow('cam1',frame1)
		cv2.imshow('cam2',frame2)
		
		

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8489))
connection = client_socket.makefile('wb')


cam = cv2.VideoCapture(0)
cam1 = cv2.VideoCapture(1)

cam.set(3, 320)
cam.set(4, 240)

cam1.set(3, 320)
cam1.set(4, 240)

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    #data = pickle.dumps(frame, 1)
    #size = len(data)
    ret1, frame1 = cam1.read()
    result1, frame1 = cv2.imencode('.jpg', frame1, encode_param)
    #data1 = pickle.dumps(frame1, 1)
    #ize1 = len(data1)
    obj=MultiCam(frame,frame1)
    data=pickle.dumps(obj,1)
    size=len(data)


  


    #print("{}: {}: {}".format(img_counter, size,size1))
    client_socket.send(struct.pack(">L", size) + data)
    #client_socket.sendall(struct.pack(">L", size1) + data1)
    img_counter += 1
    print(img_counter)


cam.release()
cam1.release()
