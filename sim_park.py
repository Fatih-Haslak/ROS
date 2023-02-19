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
from cart_sim.msg import cart_control
import math
import time
from simple_pid import PID
import sys
import warnings
#import can


warnings.filterwarnings('ignore')
empt=[]
sonuc=0
flag=0
car=1
girme=0
orta_nokta_x = 0
orta_nokta_y = 0
bridge = cv_bridge.CvBridge()
boundingBoxes=[]
boundingBoxes1=[]
myDict = {}
"""
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
"""
liste=[]
liste2=[]
flag=[]
liste3=[]
counter=0
def dedect(data):
    buffer_=20
    global temp
    global counter
    global flag
    global flag2
    global boundingBoxes
    global boundingBoxes1
    global myDict
    global msgData
    msgData = data
    print(msgData)
    boundingBoxes.clear()
    boundingBoxes1.clear()
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
    
    boundingBoxes1.append(xmin)
    boundingBoxes1.append(ymin)
    boundingBoxes1.append(xmax)
    boundingBoxes1.append(ymax)
    boundingBoxes1.append(predictVal)
    boundingBoxes1.append(predictClass)
    
    if(1):
        myDict[xmin] = [ymin,xmax,ymax] ## boundıngın x i key geri kalan values
            
       
        for i in myDict.keys(): #key lerin icine gir en buyugu bul
            print("key",i)
            liste2.append(i) # buyugu bulmak icin listeye at
            
        uzunluk=len(liste2)-2
        
        if(uzunluk>3):
            for i in range(0,uzunluk):
                liste2.pop(0)
        
        #print("Liste2",liste2)
        
        temp1=[] #listeleri birlestirmek icin
        #print("Liste2",liste2)
        temp=max(liste2) #maxini bul ve tempe at
        
        #print("Temp",temp)
        temp1.append(temp) #tempi temp1e atarak listeleri birlestir
        
        
       
        print("Dict",myDict)
        x=myDict.get(temp) #en buyuk diger degerlerimiz
        print("*-------",x)
        #print(myDict)
       
        
        if(len(liste2)>3):
            #liste2.clear()
            #myDict.clear()
            pass
            
        #print("onun",x)
        #print("Dictionary",myDict)
        
        #print("Bounding",boundingBoxes1)
      
        boundingBoxes = temp1+x #listeleri birlestir
        temp1.clear()
        tracking(boundingBoxes)
        #move(boundingBoxes)
     
def tracking()
    import cv2
    import sys

    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')￼
   

    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[2]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

    # Read video
    video = cv2.VideoCapture("videos/chaplin.mp4")

    
   

    # Read first frame.
    ok, frame = video.read()
  
    
    # Define an initial bounding box
    bbox = (boundingBoxes[0], boundingBoxes[1], boundingBoxes[2], boundingBoxes[3])

    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

  
        
# Start timer
    timer = cv2.getTickCount()

# Update tracker
    ok, bbox = tracker.update(frame)

# Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

# Draw bounding box
    if ok:
    # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
       cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    else :
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

# Display tracker type on frame
    cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

# Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

# Display result
   cv2.imshow("Tracking", frame)

# Exit if ESC pressed
   k = cv2.waitKey(1) & 0xff
   if k == 27 : break

      
    

def move(empt):                
    print("Giden veri",boundingBoxes)
    global orta_nokta_x
    global orta_nokta_y
    global dön
    global kamera_cizgisi
    global throotle
    global brake
    global center
    command=cart_control()
    x_min=0
    x_max=0
    y_min=0
    y_max=0
    

    try:
        
        x_min=empt[0]
        y_min=empt[1]
       
        x_max=empt[2]
        y_max=empt[3]
    except:
    	pass 

    #image shape (1920, 1080)
      
    ortalama=np.mean(empt[0:4])
    #distance kodunu fıratlardan al
    
    orta_nokta_x = ((x_max - x_min)/2)
    orta_nokta_y = ((y_max - y_min)/2)
    err=0.0

    print("Uzaklık",orta_nokta_x,orta_nokta_y)
    
    err1=(ortalama/10)*2 #/3

    dön=((x_min-err1)/400)

    #fren
    if(orta_nokta_y>40 and orta_nokta_x>40):#uzaklık park
        command.brake=1

    print("dön_no_pid",dön)
    
    if(orta_nokta_y>20 and orta_nokta_x>20):#uzaklık son manevra ayarlanması lazıms yeni uzaklık gelebilir.

        kamera_cizgisi=240
        
    else:
        kamera_cizgisi=310

    #0.5 1.5 1.2
    pid = PID(0.5, 1.5, 1.2, setpoint=1)
    dön=pid(dön)-err
    #print("ERR",err)
    #print("dön_pid",dön)
    
    if(x_max>(kamera_cizgisi)):
        dön=dön*-1       
    center=(int(x_min),int(y_min))
     
    print("Son_dön",dön)

    if(math.isnan(dön)==True):   
        command.brake=1
        #can     
    else:
        command.throttle=0.03
    command.steer=dön   
    pub.publish(command)
def foto(img):
    global kamera_cizgisi
    rgb_goruntu = bridge.imgmsg_to_cv2(img, "bgr8")
    print(rgb_goruntu.shape)
    #rgb_goruntu = cv2.cvtColor(rgb_goruntu, cv2.COLOR_BGR2RGB)
    cv2.imshow("asd",rgb_goruntu)
    cv2.waitKey(3)
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

    pub = rospy.Publisher('cart', cart_control, queue_size=1)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        
    cv2.destroyAllWindows() 
car
