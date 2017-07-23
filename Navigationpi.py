import os
import requests
import pymysql
import RPi.GPIO as ir
from time import sleep

ir.setwarnings(False)
ir.setmode(ir.BOARD)
ir.setup(3,ir.OUT)
ir.setup(5,ir.OUT)
ir.setup(7,ir.OUT)
ir.setup(11,ir.OUT)
ir.setup(13,ir.OUT)
ir.setup(15,ir.OUT)
ir.setup(19,ir.OUT)
ir.setup(21,ir.OUT)
ir.setup(23,ir.OUT)
ir.setup(29,ir.OUT)
ir.setup(31,ir.OUT)
ir.setup(35,ir.OUT)
ir.setup(12,ir.OUT)
ir.setup(16,ir.OUT)
ir.setup(18,ir.OUT)
ir.setup(22,ir.OUT)
ir.setup(24,ir.OUT)
ir.setup(26,ir.OUT)
ir.setup(32,ir.OUT)
ir.setup(36,ir.OUT)
ir.setup(38,ir.OUT)
ir.setup(40,ir.OUT)
ir.setup(33,ir.OUT)
ir.setup(37,ir.IN)

ir.output(35,ir.HIGH)
circum=0.4
db=pymysql.connect(## Enter the Database connection Credentials to connect )
cursor =db.cursor()

direction=[]
distance=[]
parity_bit=[]

print("Dateabse Connected")

sql="""SELECT * FROM NAVIGATION"""

try:
    cursor.execute(sql)
    results=cursor.fetchall()
except:
    print("Database Not Connected Proparly")

noofsteps=len(results)

for val in results:
    direction.append(str(val[1]))
    distance.append(int(val[2]))
    parity_bit.append(int(val[3]))
    
print("Results fetched")
#print(direction)
#print(distance)
#print(parity_bit)

def stop():
    print("Stop")
    ir.output(3,ir.LOW)
    ir.output(5,ir.LOW)
    sleep(1)
    
def forward(value):
    print("Forward "+str(value))
    ir.output(3,ir.HIGH)
    ir.output(5,ir.HIGH)
    print(value)
    value-=circum
    print(value)
    while value>=0:
        if ir.input(37):
            ir.output(3,ir.LOW)
            sleep(0.05)
            ir.output(3,ir.HIGH)
            value-=circum
            print(value)
    print(value)
    print("value satisfied")
    stop()

def right(value):
    print("Right "+str(value))
    ir.output(3,ir.HIGH)
    sleep(1.8)
    stop()
    forward(value)
    

def left(value):
    print("Left "+str(value))
    ir.output(5,ir.HIGH)
    sleep(1.8)
    stop()
    forward(value)


if all(i==1 for i in parity_bit):
    print("Parity_bit = 1")
    i=0
    while i<len(direction):
        if direction[i] == "STRAIGHT":
            forward(distance[i])
        elif direction[i] =="RIGHT":
            right(distance[i])
        elif direction[i] =="LEFT":
            left(distance[i])
        i+=1
    stop()
    sql="UPDATE NAVIGATION SET PARITY_BIT = 0 WHERE PARITY_BIT = 1"
    try:
        cursor.execute(sql)
        db.commit()
        print("Changes Made successfully")
    except:
        print("Unable to make the changes")
        db.rollback()
else:
    print("Parity_Bit still 0")
        
db.close()

os.system("python3 /home/pi/Desktop/control_gpio/initial_check.py") ## Check this Path
