#author fatih
import torch
import cv2
import pandas as pd
import numpy as np
from sensor_msgs.msg import Image
import ros_numpy
import rospy
from std_msgs.msg import String, Int32MultiArray
import warnings
warnings.filterwarnings('ignore')
count=0
temp=0
# Model 
model = torch.hub.load('/home/fatih/yolov5', 'custom', path='/home/fatih/Desktop/model/best.pt', source='local')
image_publish = rospy.Publisher("camera_detect",Image,queue_size=10)
boundingBoxes_publish = rospy.Publisher("boundingBoxes",String,queue_size = 10)
oran_publish = rospy.Publisher("oran",String,queue_size = 10)
gir=0
tespit_edilen = ""
oran = ""
orta_nokta_x = 0
orta_nokta_y = 0
def detect(data):
	global temp
	global count
	global gir
	boundingData=''
	np_img = ros_numpy.numpify(data)
	np_img = cv2.resize(np_img,((480,480)))
	results = model(np_img)
	data = results.pandas().xyxy[0]
	data = data.to_numpy()
	global tespit_edilen
	global orta_nokta_x
	global orta_nokta_y
	for box in data:
		if(str(box[6])=="park"):
			orta_nokta_x = ((box[2] - box[0])/2)
			orta_nokta_y = ((box[3] - box[1])/2)
			#print(orta_nokta_x, orta_nokta_y)
			if 1:
				#xmin,ymin,xmax,ymax,predictVal,predictClass
				boundingData=str([int(box[0]),int(box[1]),int(box[2]),int(box[3]),str(box[4]),str(box[6])])

				start_point =(int(box[0]),int(box[1]))
				end_point = (int(box[2]),int(box[3]))
				start_point_putText =(int(box[0]-5),int(box[1]-5))
				cv2.rectangle(np_img, start_point, end_point,(0, 255, 0), 2)
				cv2.putText(np_img, box[6], start_point_putText, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255,0), 3)
				
				cv2.rectangle(np_img, start_point, end_point,(0, 255, 0), 2)
				cv2.putText(np_img, str(box[6]), start_point_putText, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255,0), 3)

		#print(tespit_edilen,'%.2f' %(oran))
		#print(data)

				msg = ros_numpy.msgify(Image, np_img[...,:3], encoding='rgb8')
				if(boundingData!=''):
					boundingBoxes_publish.publish(boundingData)  
					image_publish.publish(msg)
def sonlandir():
    rospy.loginfo('sonlandirildi')

if __name__ == "__main__":
    rospy.init_node('camera_yolov5',anonymous=True)

    rospy.on_shutdown(sonlandir)

    rospy.Subscriber('/cart/front_camera/image_raw',Image,detect)
    rospy.spin()
