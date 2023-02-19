#author @Fatih
import os
from PIL import Image

# Function to rename multiple files
dataset="C:\\Users\\90546\\OneDrive\\Masaüstü\\sıgun_kod\\resize_to"
dataset1="C:\\Users\\90546\\OneDrive\\Masaüstü\\sıgun_kod\\resize_to_new_name"


count=0
for filename in (os.listdir(dataset)):
    if filename.endswith(".jpg"):
        count=count+1
        print(count)
        dst = "unı" + str(count) + ".jpg"
        dst=os.path.join(dataset1, dst) 
        completeName = os.path.join(dataset, filename)
        src =completeName
        #print(src)
        #print(dst)
        os.rename(src, dst)

count1=0
for file in (os.listdir(dataset)):
    if file.endswith(".txt"):
        count1=count1+1
        print(count1)
        dst1 = "unı" + str(count1) + ".txt"
        dst1=os.path.join(dataset1, dst1) 
        completeName = os.path.join(dataset, file)
        src1 =completeName
        #print(src1)
        #print(dst1)
        os.rename(src1, dst1)
        print("kaydetti")


