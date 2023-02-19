import os
import numpy as np
sayac=0
dataset_path ="C:\\Users\\90546\\OneDrive\\Masaüstü\\sıgun_kod\\standart"#PATHI VERDIM ANCAK KODU YINE O KLASORUN ICINDE CALISTIRILMASI LAZIM
liste=[]
liste2=[]
bulundu=0
classlar=[]
dosya_isimleri=[]
kır=0
tüm_txtler=[]
#55.SATIRDA SILMEK ISTEDIGIN CLASSLARI GIREBILIRSIN
#GORUNTULER PNG FORMATINDA OLMALI
for file in os.listdir(dataset_path):
  
    if file.endswith(".txt"):
        tüm_txtler.append(os.path.join(file))
        pathh=str(dataset_path)
        dosya=str(file)  
        fihrist = open(file,"r")
        liste.append(fihrist.readline())#liste ıcınde dosyanın ılk satırı bulunmakta
       
        #silincek txt bulma ve yazma kodu
        if(1==1):  
            while(True):

               try:          
                    bulundu=0
                    #print("Liste",liste[0][sayac])
                    liste2.append(liste[0][sayac])#tek tek eklıyoruz satırın charlarını
                    sayac=sayac+1
                    if(liste[0][sayac]==" "):#bosluga denk geldıysek duruyoruz ıstedıgımız class kodu bulundu
                        #print("Bosluk")
                        #print("liste2",liste2)
                        if(len(liste2)==1):#eger tek hanelı ıse
                            #print(int(liste2[0]))
                            classlar.append(int(liste2[0]))#ekledık
                        elif(len(liste2)==2):#cıft hanelı ise              
                            #print(int(liste2[0]+liste2[1]))
                            classlar.append(int(liste2[0]+liste2[1]))#str toplayıp ekledık int(olarak)
                        else:
                            bulundu=0
                        bulundu=1#bulduysak temızlıyoruz her seyı tekrar yenısını bulmak ıcın
                    
                    if(bulundu==1):
                            liste.clear()
                            liste2.clear()
                    
                            liste.append(fihrist.readline())#dıger satıra gecıyoruz

                            #print("deneme",liste)
                            sayac=0
                    for i in classlar:
                        if(i==3 or i==4 or i==9 or i==10 or i==11 or i==13 or i==16 or i==17 or i==20 or i==21 or i==22 or i==23):#SILMEK ISTEDIGIN CLASSLAR
                                #notlu halı hıc sılmeden sadece yazılcakları txt ıcıne at
                            dosya_isimleri.append(os.path.join(file))#sılmek ıstedıgımız txtlerı buraya atadık
                            if(i==2):
                                #satı_silincek
                                pass
                        else:
                            print("Classlar",classlar)
                        classlar.clear()
                             
                        
               except:
                   
                   liste.clear()
                   liste2.clear()
                   classlar.clear()
                   break
                                          
#silincek txt listesi
silincek_txtler=list(set(dosya_isimleri))#sılıncek txtlerde tekrar eden oldugu ıcın teke ındırdık
sil_txt=[]
#print("Silincek",silincek_txtler)

#silince png listesi txt to png
try:
    arr = np.char.replace(silincek_txtler, 'txt', 'png')#resım dosyalarını sılmek ıcın ısımlerı txt den png cevırdık
    arr2 = np.char.replace(silincek_txtler, 'txt', 'jpg')
    ar2=list(arr)#tekrar listeye cevırdık
    arrr3=list(arr2)
    print("Pngler",ar2)
except:
    print("Belirtilen classlar bulunamadı")
    ar2=[]
    pass
#silme kodları
ana_Dizin=os.listdir(dataset_path)

for i in ana_Dizin:
    for a in silincek_txtler:
        if(i==a):
           #print("eşlesdi")
           os.remove(i)

for i in ana_Dizin:
    for a in ar2:
        if(i==a):
            #print("png_sil")
            os.remove(i)
try:
    for i in ana_Dizin:
        for a in arrr3:
            if(i==a):
                #print("png_sil")
                os.remove(i)
except:
    pass
