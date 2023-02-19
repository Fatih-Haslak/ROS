from PIL import Image
import os

dataset_path ="C:\\Users\\90546\\OneDrive\\Masaüstü\\sıgun_kod\\resize_foto"#nerdekı
dataset_path1 ="C:\\Users\\90546\\OneDrive\\Masaüstü\\sıgun_kod\\resize_to"#nereye kaydetcen
for file in os.listdir(dataset_path):
   
    if file.endswith(".png"):

        print(file)
        im1 = Image.open(os.path.join(dataset_path,file))
          

        name = file[:-4]
        completeName = os.path.join(dataset_path1, name)       
        im1.save(completeName + '.jpg')
    if file.endswith(".jpg"):
        print(file)
        im1 = Image.open(os.path.join(dataset_path,file))
        name = file[:-4]
        completeName = os.path.join(dataset_path1, name)       
        im1.save(completeName + '.jpg')
