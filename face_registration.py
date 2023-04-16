import cv2 as cv
import numpy as np
from menu import *
from time import sleep
import os

def FaceRegistration(reg_img_num,cascade_path,export_path,Id,users_file_path):# arc regisztráló függvény
    
    face_cascade = cv.CascadeClassifier(cascade_path)
    pictures = []
    pic_num = 0
    ShowSlidingMessage(" Kérem nyomja meg a zöld gombot a '+' jel pislogásnál! Szükséges készíteni "+ str(reg_img_num)+ " sikeres képet!")
    close = False
    while pic_num<reg_img_num and not close:
        status = Blinking("+",1)
        if status == 1:
            cap = cv.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            cv.destroyAllWindows()
            detected_face = face_cascade.detectMultiScale(frame,1.1,3,minSize=(80,80))
            if len(detected_face) == 1:
                pic_num += 1
                pictures.append(frame)
                ShowMessage("lementet kép("+str(pic_num)+")")
                sleep(0.5)
            else:
                ShowMessage("nincs arc!")
                sleep(0.5)
        elif status == 2:
            close = True
    if not close and len(pictures) == reg_img_num:
    
        for i in range(len(pictures)):
            cv.imwrite(export_path+str(Id)+"_"+str(i)+".jpg", pictures[i])
        file = open(users_file_path, 'a')
        file.write(str(Id)+":névtelen\n")
        file.close()
        return True
    else:
        return False
    