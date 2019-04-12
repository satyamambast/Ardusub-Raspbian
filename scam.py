import socket
import pickle
import threading
import time
import struct
import io
import cv2
import serial

host = ('192.168.2.2',5058)
global conn,addr,k,msg1
print("xxxxx")
sock2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock2.bind(host)
sock2.listen(5)
conn,addr=sock2.accept()
ser = serial.Serial('/dev/ttyUSB0',9600)

def arduino(x):
    print("1")
    print("scam:",x)
    print("2")
    if(x==1):               #forward move8ment 2 min_rov 
        ser.write(b'1')
        time.sleep(1)
    if(x==2):               #backward movement 2 min_rov 
        ser.write(b'2')
        time.sleep(1)
    if(x==3):
        ser.write(b'3')     #forward movement of spool
        time.sleep(1)
    if(x==4):
        ser.write(b'4')     #backward movement of spool
        time.sleep(1)
    if(x==0):               #for stopping all motors of min_rov and spool
        ser.write(b'0')
        time.sleep(1) 
    if(x==3):               #for manipulator forward movement
        ser.write(b'5')
        time.sleep(1)
    if(x==4):               #for manipulator backward movement
        ser.write(b'6')
        time.sleep(1)
    if(x==5):               #for stopping the movement of the manipulator
        ser.write(b'7')
        time.sleep(1)
    k = ser.readline()
    #m = ser.readline()
    return k
 

def receive_controller_data():
    global msg1
    sock1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock1.connect(('192.168.2.1',5059))
    while True:
        msg=sock1.recv(1024)
        msg1 = pickle.loads(msg)
        print("aman : ",msg1)
        #ard = msg1[-1]
        time.sleep(.01)


def send_sensor_values():
    temp = arduino(1) 
    while True:
        list1 = [temp]
	print("alive: ",send_sense.is_alive())
        data = pickle.dumps(list1)
        conn.send(data)
        time.sleep(.01)

'''
def send_frame():
    client_socket = socket.socket(socket.AF_INET, sock.SOCK_STREAM)
    client_socket.connect(('192.168.2.1', 5003))

    cam = cv2.VideoCapture(1)
    cam.seet(3,320)
    cam.set(4, 240)
    img_counter = 0
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    
    while True:
        ret, frame = cam.read()
        result, frame = cv2.inencode('.jpg', frame, encode_param)
        size = len(data)

        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L",size) + data)
        img_counter += 1
    cam.release()
'''    
    
recv_cont = threading.Thread(target = receive_controller_data, args = ())
send_sense = threading.Thread(target = send_sensor_values, args = ())
#ard = threading.Thread(target = arduino, args = (1))
#send_cam = threading.Thread(target = send_frame, args = ())

recv_cont.start()
send_sense.start()
#ard.start()
#send_cam.start()

