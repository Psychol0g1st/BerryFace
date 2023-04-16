import os
import numpy as np
import cv2 as cv
from menu import *

original_img_path = "/home/pi/Desktop/FaceRec/BerryFace/Faces/original/"
cropped_img_path = "/home/pi/Desktop/FaceRec/BerryFace/Faces/cropped/"
unknown_img_path = "/home/pi/Desktop/FaceRec/BerryFace/Faces/unknown/"

def GetImageNum(path):#Megadja a képek számát agott elérési útvonalon
    face_files = os.listdir(path)#beolvassa a állomány neveket adott útvonalon
    img_count = len(face_files)
    return img_count, face_files
def CropImages(img_num, new_width,new_height,import_path,export_path, cascade_path,Id):#A képeken megtalálja az arcot és csökkenti a méretét a megadott értéknek megfelelően
    Id -= 1
    face_dir = import_path
    face_files = os.listdir(face_dir)
    export_dir = export_path

    for face in face_files:

        name = os.path.basename(face)
        name = name.split('.')[0]
        to_crop = name.split('_')[0]
        if int(to_crop) == Id:
            opened_image = cv.imread(face_dir+face)
            opened_image = cv.cvtColor(opened_image, cv.COLOR_BGR2GRAY)
            image = np.array(opened_image, 'uint8')
            face_cascade = cv.CascadeClassifier(cascade_path)#deklarálja a Kaszkád osztályt, amely elvégzi az arc keresést a paraméterbe megadott kaszkádnak megfelelően
            detected_faces = face_cascade.detectMultiScale(image)#Kaszkád alkalmazása a képen
            for (column, row, width, height) in detected_faces:
                cropped_image = image[row:row+height, column:column+width]
                resized_image = cv.resize(cropped_image, (new_width, new_height), interpolation=cv.INTER_CUBIC)#kép méretezése
                cv.imwrite(export_dir+name+'.jpg',resized_image)#kép mentése
    cv.destroyAllWindows()
    
def ReadCroppedImgs(path, img_num, height, width):#Méretezett képek beolvasása
    if img_num>0:
        face_files = os.listdir(path)
        face_data = np.ndarray(shape=(img_num, height*width), dtype=np.float64) #definiál tömböt ami képvektorokat fog tartalmazni
        for i in range(img_num):
            img = cv.imread(path + face_files[i])#beolvassa a képet
            img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)#Szürke színformátumba konvertálja
            face_data[i] = np.array(img, dtype=float).flatten()#2D képet vektorrá alakjtja
        return face_data
    else:
        ShowMessage("Nincs kép!")

def InitMeanFace(width, height):#átlag arcvektor deklarálása
    mean_face = np.ndarray(width*height, dtype=float)
    return mean_face

def InitEigenFaces(n_components, width, height):#sajátarc vektortömb deklarálása
    eigenfaces = np.ndarray((n_components,width*height), dtype=float)
    return eigenfaces

def InitWeights(n_components, img_num):#súly vektortömb deklarálása
    weights = np.ndarray((img_num,n_components), dtype=float)
    return weights
def SetId(file):#Legútóbbi ID értéke beállítása
    f = open(file,'r')
    Id = f.readline()
    f.close()
    return int(Id)
def SaveId(file, Id):#Legútóbbi ID értéke mentése
    f = open(file,'w')
    f.write(str(Id))
    f.close()