# -*- coding: utf-8 -*-

from cmath import nan
from curses.ascii import ETB
from pickle import GLOBAL, TRUE
from tkinter import N
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError
import rospy
from std_msgs.msg import String
import tf
import torch
import cv2
import pandas as pd
import numpy as np
from sensor_msgs.msg import Image
import ros_numpy
import rospy
#from cart_sim.msg import cart_control
import math
import time
from simple_pid import PID
import sys
import warnings
import can


warnings.filterwarnings('ignore')
empt=[]
sonuc=0
flag=0
car=1
sayac=0
girme=0
orta_nokta_x = 0
orta_nokta_y = 0
bridge = cv_bridge.CvBridge()


bustype = 'socketcan'
channel = 'can0'
operational = 1
steering_angle = 128
throttle = 128
brake = 0 #255 en ideali


def car_stop():
    brake=255
    operation = 0
    bus = can.interface.Bus(channel=channel, bustype=bustype)
    msg = can.Message(arbitration_id=0x560,is_extended_id=False, data=[operational,steering_angle,throttle,brake])
    try:
        bus.send(msg)
        print("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")


def car_control(steering_angle,throttle,brake=0):
    bus = can.interface.Bus(channel=channel, bustype=bustype)
    msg = can.Message(arbitration_id=0x560,is_extended_id=False, data=[operational,steering_angle,throttle,brake])
    try:
       bus.send(msg)
       #print("Message sent on {}".format(bus.channel_info))
       time.sleep(0.03)
    except can.CanError:
       print("Message NOT sent")


def dedect(data):
    global boundingBoxes
    global msgData
    msgData = data
    boundingBoxes.clear()

    veri = str(data).split("[")[1]
    veri = veri.split("]")[0]
    veri = veri.split(",")
    veri[4]=float(veri[4].split("\'")[1])
    veri[5]=str(veri[5].split("\'")[1])

    xmin = int(veri[0])
    ymin = int(veri[1])
    xmax = int(veri[2])
    ymax = int(veri[3])
    predictVal = veri[4]
    predictClass = veri[5]

    boundingBoxes.append(xmin)
    boundingBoxes.append(ymin)
    boundingBoxes.append(xmax)
    boundingBoxes.append(ymax)
    boundingBoxes.append(predictVal)
    boundingBoxes.append(predictClass)
    move(boundingBoxes)
    boundingBoxes.clear()
    

def move(empt):
    global orta_nokta_x
    global orta_nokta_y
    global dön
    global kamera_cizgisi
    global throotle
    global brake
    global center

    x_min=0
    x_max=0
    y_min=0
    y_max=0
    

    try:
        
        x_min=empt[0]
        y_min=empt[1]
       
        x_max=empt[0]+empt[2]
        y_max=empt[1]+empt[3]
    except:
    	pass 

    #image shape (1920, 1080)
      
    ortalama=np.mean(empt)
    #distance kodunu fıratlardan al
    
    orta_nokta_x = ((x_max - x_min)/2)
    orta_nokta_y = ((y_max - y_min)/2)
    err=0.0

    print("Uzaklık",orta_nokta_x,orta_nokta_y)
    
    err1=(ortalama/10)*2 #/3

    dön=((x_min-err1)/400)*255
    if(dön<128):
        print("128'den kücük geldi")

    #fren
    if(orta_nokta_y>18 and orta_nokta_x>18):#uzaklık park
        car_stop()

    print("dön_no_pid",dön)
    
    if(orta_nokta_y>7.7 and orta_nokta_x>7.7):#uzaklık son manevra ayarlanması lazıms yeni uzaklık gelebilir.

        kamera_cizgisi=240
        
    else:
        kamera_cizgisi=310

    #0.5 1.5 1.2
    pid = PID(0.5, 1.5, 1.2, setpoint=1)
    dön=pid(dön)-err
    #print("ERR",err)
    #print("dön_pid",dön)
    
    if(x_max>kamera_cizgisi):
        dön=(dön/255)*60
        print("Sağ,Dön",dön)
    center=(int(x_min),int(y_min))
     
    print("Son_dön",dön)

    if(math.isnan(dön)==True):   
        car_stop()
        #can     
    else:
        throttle=0.03*255
        #can
    steering=dön
    steering=abs(int(steering)
    car_control(steering,138)
def foto(img):
   
    rgb_goruntu = bridge.imgmsg_to_cv2(img, "bgr8")
    #print(rgb_goruntu.shape)
    #rgb_goruntu = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    
    start_point = (kamera_cizgisi, 0)
    end_point = (kamera_cizgisi, 240)
    renk=(155,255,255)
    if(kamera_cizgisi<240):
        renk=(0,0,0)
    
    image = cv2.line(rgb_goruntu, start_point, end_point, renk, 2)

    cv2.imshow("__",rgb_goruntu)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        return 0

def sonlandir():
    rospy.loginfo('sonlandirildi')

if __name__ == "__main__":

    rospy.init_node('camera_yolov5',anonymous=True)

    rospy.loginfo('sonlandırmak için CTRL+C')    
    rospy.on_shutdown(sonlandir)

    rospy.Subscriber('boundingBoxes',String,dedect)
    rospy.Subscriber('camera_detect',Image,foto)

    #pub = rospy.Publisher('cart', cart_control, queue_size=1)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        car_stop()
    cv2.destroyAllWindows() 
