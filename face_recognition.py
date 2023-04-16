import numpy as np
from matplotlib import pyplot as plt
from calculation import euclidean
import cv2 as cv
from menu import *
from datetime import datetime

def FaceRecognition(img_count, mean, eigenfaces, w, threshold,cascade_path,cropped_width, cropped_height, unknown_path, users_file_path, file_names):#arc felismerő függvény
    recognised_id = -1
    close = False
    face_cascade = cv.CascadeClassifier(cascade_path)
    cap = cv.VideoCapture(0)#kamera vezérlési osztály
    cap.set(cv.CAP_PROP_BUFFERSIZE, 1)#elkészített képek tárolási darabszáma:1
    capture = True
    while not close:
        Blinking("arc kereses",0)
        if not capture:
            cap = cv.VideoCapture(0)
            cap.set(cv.CAP_PROP_BUFFERSIZE, 1)
            capture = True
        ret, frame = cap.read()
        detected_face = face_cascade.detectMultiScale(frame,1.1,3,minSize=(80,80))#arckeresés a képkockán
        if len(detected_face) == 1: #ha talál arcot a képen akko:
            cap.release()
            capture = False
            cv.waitKey(100)
            for (column, row, width, height) in detected_face:
                #elvégzi az Eigenface felismerési algoritmus lépéseit
                unknown_person = cv.resize(frame[row:row+height, column:column+width], (cropped_width, cropped_height), interpolation=cv.INTER_CUBIC)
                unknown_person = cv.cvtColor(unknown_person, cv.COLOR_BGR2GRAY)
                unknown_person = unknown_person.flatten()
                unknown_normalised = unknown_person - mean
                unknown_w = np.array(np.dot(eigenfaces,unknown_normalised.transpose()))
                unknown_w = unknown_w.flatten()
                first_value = True
                for j in range(img_count):
                    dist = euclidean(unknown_w, w[j])
                    if first_value and dist != 0:
                        min_dist = dist
                        first_value = False
                    elif dist != 0:
                        if min_dist > dist:
                            min_dist = dist
                            recognised_id = j
                now = datetime.now()
                date_stamp = now.strftime("%d_%m_%Y_%H_%M_%S")
                if(min_dist > threshold):
                    ShowMessage("ismeretlen!")
                    cv.imwrite(unknown_path+date_stamp+".jpg", frame)#lementi az ismeretlen arcot
                    cv.waitKey(1000)
                else:      
                    ShowMessage("ismert!")
                    file = open(users_file_path, 'r')
                    for line in file:
                        values = line.split(":")
                        if values[0] == file_names[recognised_id].split("_")[0]:
                            ShowSlidingMessage("üdvözlöm "+values[1])
                            break
                    cv.waitKey(1000)
            
        close = Close()#(menu.py)kilépést ellenőrző függvént
    if capture:
        cap.release()
    cv.destroyAllWindows()