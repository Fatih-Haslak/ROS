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


sonuc=0
flag=0
car=1
sayac=0
girme=0
orta_nokta_x = 0
orta_nokta_y = 0
bridge = cv_bridge.CvBridge()
warnings.filterwarnings('ignore')
empt=[]
sonuc=0
flag=0
tracker_=[]
bridge = cv_bridge.CvBridge()
boundingBoxes=[]
boundingBoxes1=[]
kontrol_tracker=0
tracker_kontrol=0


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

liste=[]
liste2=[]
flag=[]
liste3=[]
counter=0
def dedect(data):
    buffer_=20
    global tracker_
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
    global kontrol_tracker
    if(1):    
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
        #boundingBoxes1.append(predictVal)
        #boundingBoxes1.append(predictClass)
   
        if(kontrol_tracker==0 and len(boundingBoxes1)!=0):
            tracker_=boundingBoxes1
            print("Tracker --->",tracker_)
            kontrol_tracker=1
       

def foto(img):
    global kamera_cizgisi
    rgb_goruntu = bridge.imgmsg_to_cv2(img, "bgr8")
    #print(rgb_goruntu.shape)
    #rgb_goruntu = cv2.cvtColor(rgb_goruntu, cv2.COLOR_BGR2RGB)
    #cv2.imshow("asd",rgb_goruntu)
    cv2.waitKey(3)
    #start_point = (kamera_cizgisi, 0)
    #end_point = (kamera_cizgisi, 240)
    renk=(155,255,255)
    #if(kamera_cizgisi<240):
        #renk=(0,0,0)
    
    #image = cv2.line(rgb_goruntu, start_point, end_point, renk, 2)

    #cv2.imshow("__",rgb_goruntu)
    tracking(rgb_goruntu)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        return 0
    
def tracking(frame):
    global tracker_
    global tracker
    global tracker_kontrol
    import sys

    #(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')￼
    if(tracker_kontrol==0):

        tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
        #tracker_type = tracker_types[0]

        if 1:
            tracker = cv2.legacy_TrackerMedianFlow.create()
        

 
        # Define an initial bounding box
        try:
            bbox = (tracker_[0], tracker_[1], int(tracker_[2]-tracker_[0]) , int(tracker_[3]-tracker_[1]))  
            print("bounding_box",bbox)
            print("jkh")
        except:
            print("tespit yok")
        # Uncomment the line below to select a different bounding box
        #bbox = cv2.selectROI(frame)
        print("book",bbox)
        # Initialize tracker with first frame and bounding box
        
        ok = tracker.init(frame, bbox)
        #print("Takip,,,",bbox)
        tracker_kontrol=1
      

# Update tracker
    ok, bbox = tracker.update(frame)
    #print("book",bbox)
      
# Draw bounding box
    if ok:
    # Tracking success
        move(bbox)
        print("x_min",bbox[0])
        print("y_mİn",bbox[1])
        print("x_max",int(bbox[0]+ bbox[2]))
        print("y_max",int(bbox[1] + bbox[3]))
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,255,0), 2, 1)
    else :
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (480,480), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)


    #result
    cv2.imshow("Tracking", frame)
  


      
 
    


def move(empt):                
    print("Giden veri",boundingBoxes)
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
      
    ortalama=(x_min+y_min+x_max+y_max)/4
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
    if(orta_nokta_y>18 and orta_nokta_x>18): #uzaklık park
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
    
    if(x_max>(kamera_cizgisi)):
        dön=(dön/255)*60
        print("Sağ,Dön",dön)   
    center=(int(x_min),int(y_min))
     
    print("Son_dön",dön)

    if(math.isnan(dön)==True):   
        car_stop()
        #can     
    else:
        command.throttle=0.03*255
    steering=dön
    steering=abs(int(steering)
    car_control(steering,138)

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
        
    cv2.destroyAllWindows() 
car
