import serial
import time

ser = serial.Serial('/dev/ttyUSB3',9600)
def cont(t):
    while True:
        t = int(input('Enter 0 to 7-->\n'))
        if(t==1):               #forward move8ment 2 min_rov 
            ser.write(b'1')
            time.sleep(1)
        if(t==2):               #backward movement 2 min_rov 
            ser.write(b'2')
            time.sleep(1)
        if(t==3):
            ser.write(b'3')     #forward movement of spool
            time.sleep(1)
        if(t==4):
            ser.write(b'4')     #backward movement of spool
            time.sleep(1)
        if(t==0):               #for stopping all motors of min_rov and spool
            ser.write(b'0')
            time.sleep(1) 


        if(t==3):               #for manipulator forward movement
            ser.write(b'5')
            time.sleep(1)
        if(t==4):               #for manipulator backward movement
            ser.write(b'6')
            time.sleep(1)
        if(t==5):               #for stopping the movement of the manipulator
            ser.write(b'7')
            time.sleep(1)
        
        k = ser.readline()
        l = ser.readline()
        print(k)
        print(l)
    
cont(1)
