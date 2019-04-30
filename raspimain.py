
import socket
import pickle
import threading
import time
import struct
import io
import cv2
import serial
l1=0
l2=1
l3=2
boro=3
class MultiCam:
    
    def __init__(self):
        self.frame1=None
        self.frame2=None
        self.frame3=None
        self.frame4=None
        self.ret1=False
        self.ret2=False
        self.ret3=False
        self.ret4=False
    
    def encodepossible(self,cam1,cam2,cam3,cam4):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        if msg1[-1]==0:
            if cam4.isOpened():
                cam4.release()
                cam1.open(l1)
                cam2.open(l2)
                cam3.open(l3)
            elif not cam1.isOpened():
                cam1.open(l1)
                cam2.open(l2)
                cam3.open(l3)
                
                
            self.ret1, frame1 = cam1.read()
            self.ret2, frame2 = cam2.read()
            self.ret3, frame3 = cam3.read()
            #self.ret4, frame4 = cam4.read()
            if self.ret1:
                result, self.frame1 = cv2.imencode('.jpg', frame1, encode_param)            
            elif self.ret2:
                result, self.frame2 = cv2.imencode('.jpg', frame2, encode_param)            
            elif self.ret3:
                result, self.frame3 = cv2.imencode('.jpg', frame3, encode_param)
        else:
            if cam1.isOpened():
                cam1.release()
                cam2.release()
                cam3.release()
                cam4.open(boro)
            self.ret4,frame4=cam4.read()        
            if self.ret4:
                result, self.frame4 = cv2.imencode('.jpg', frame4, encode_param)            

    def testing(self,cam1):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        self.ret1, frame1 = cam1.read()
        result, self.frame1 = cv2.imencode('.jpg', frame1, encode_param)
        self.frame2=self.frame3=self.frame1
        self.ret2=self.ret3=self.ret1
    def displayallfeeds(self):
	    cv2.imshow('cam1',self.frame1)
	    cv2.imshow('cam2',self.frame2)
	    cv2.imshow('cam3',self.frame3)
	    cv2.imshow('cam4',self.frame4)

host = ('192.168.2.2',5070)
global conn,addr,k
msg1=[]
print("xxxxx")
sock2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock2.bind(host)
sock2.listen(5)
conn,addr=sock2.accept()
ser = serial.Serial('/dev/ttyUSB0',9600)

def arduino(x):
    print("scam:",x)
    if len(x)==0:
        k = ser.readline()
        return k
    if(x[8]==1):               #forward move8ment 2 min_rov Y 
        ser.write(b'1')
        time.sleep(1)
    if(x[5]==1):               #backward movement 2 min_rov A
        ser.write(b'2')
        time.sleep(1)
    if(x[10]==1):
        ser.write(b'3')     #forward movement of spool
        time.sleep(1)
    if(x[9]==1):
        ser.write(b'4')     #backward movement of spool
        time.sleep(1)
    if(x[6]==1):               #for stopping all motors of min_rov and spool
        ser.write(b'0')
        time.sleep(1) 
    if(x[2]==-1):               #for manipulator forward movement
        ser.write(b'5')
        time.sleep(1)
    if(x[2]==1):               #for manipulator backward movement
        ser.write(b'6')
        time.sleep(1)
    if(x[7]==1):               #for stopping the movement of the manipulator
        ser.write(b'7')
        time.sleep(1)
    k = ser.readline()
    m = ser.readline()
    return k,m
 

def receive_controller_data():
    global msg1
    sock1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock1.connect(('192.168.2.1',5059))
    while True:
        msg=sock1.recv(1024)
        try:
            msg1 = pickle.loads(msg)
        except:
            time.sleep(2) #if controller disconnects
        print("aman : ",msg1)
        #ard = msg1[-1]
        time.sleep(.01)


def send_sensor_values():
    global msg1 
    while True:
        temp,metal = arduino(msg1)
        list1 = [temp,metal]
        #print("alive: ",send_sense.is_alive())
        data = pickle.dumps(list1)
        conn.send(data)
        time.sleep(.01)

def send_frame():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.2.1', 5004))
    cam1 = cv2.VideoCapture(l1)
    cam1.set(3,320)
    cam1.set(4, 240)
    cam2 = cv2.VideoCapture(l2)
    cam2.set(3,320)
    cam2.set(4, 240)
    cam3 = cv2.VideoCapture(l3)
    cam3.set(3,320)
    cam3.set(4, 240)
    cam4 = cv2.VideoCapture(boro)
    cam4.set(3,320)
    cam4.set(4, 240)
    cam4.release()
    img_counter = 0
    while True:
        obj=MultiCam()
        obj.encodepossible(cam1,cam2,cam3,cam4)
        #obj.testing(cam1)
        #ret, frame = cam.read()
        #result, frame = cv2.inencode('.jpg', frame, encode_param)
        data=pickle.dumps(obj,1)
        size = len(data)

        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L",size) + data)
        img_counter += 1
    cam1.release()
    cam2.release()
    cam3.release()
    cam4.release()
    
recv_cont = threading.Thread(target = receive_controller_data, args = ())
send_sense = threading.Thread(target = send_sensor_values, args = ())
#ard = threading.Thread(target = arduino, args = (1))
send_cam = threading.Thread(target = send_frame, args = ())

recv_cont.start()
send_sense.start()
#ard.start()
send_cam.start()
