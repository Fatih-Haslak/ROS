
import os
from PIL import Image

f = r"C:\Users\90546\OneDrive\Masaüstü\sıgun_kod\test"    #Enter the location of your Image Folder
f_save=r"C:\Users\90546\OneDrive\Masaüstü\sıgun_kod\resize_foto"

width = 416
height = 416
dim = (width, height)
for file in os.listdir(f):
    if file.endswith(".png"):
        f_img = f+'/'+file#os.path.joın
        print(f_img)

        try:
            img = Image.open(f_img)
            img = img.resize(dim)
            completeName = os.path.join(f_save, file)       
            img.save(completeName)
        except IOError:
            print("error")
            pass
    
    if file.endswith(".jpg"):
        f_img = f+'/'+file#os.path.joın
        print(f_img)

        try:
            img = Image.open(f_img)
            completeName = os.path.join(f_save, file)       
            img.save(completeName)
        except IOError:
            print("error")
            pass
