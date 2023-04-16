import numpy as np
import os
import cv2 as cv

def euclidean(a,b):#Euklídési távolságot számoló függvény
  a = np.array(a)
  b = np.array(b)
  sum = 0
  for i in range(a.shape[0]):
    sum += np.power((a[i] - b[i]),2)
  return np.sqrt(sum)

def Calculation(width, height, principal_component_num, img_num, training_data):#Eigenface algoritmus számolást elvégző függvény
    eigenfaces = []
    mean, EigenVector = cv.PCACompute(training_data, mean=None,maxComponents=principal_component_num)#Átlag arcvektor, Sajátvektorok számolása, rendezése sajátértékeknek megfelelően, kiválaszt n darab vektort
    normalised_train_data = np.subtract(training_data,mean)#normalizált arcvektorok számolása
    i=0

    for eigenVector in EigenVector:
        eigenfaces.append(eigenVector)
        i+=1
    w = np.array([np.dot(eigenfaces,i) for i in normalised_train_data]) #súlyok számolása
    #Határérték meghatározása
    distances_vector = np.ndarray(img_num, dtype=float)#távolság vektor amelybe tárolom minden kép egymástól való Euklidészi távolságot
    dist_num = 0
    min_dist = 0
    for i in range(img_num):
        first_value = True
        for j in range(img_num):
            if i == j:
                continue
            dist = euclidean(w[i], w[j])
            if first_value and dist != 0:
                min_dist = dist
                first_value = False
            elif dist != 0:
                if min_dist > dist:
                    min_dist = dist
        #print(min_dist)
        distances_vector[dist_num] = min_dist
        dist_num += 1
    max_from_all = max(distances_vector)#összes közül kiválasztja a legnagyobbat
    threshold = max_from_all*0.7# veszi a 70%-át a kiszámolt értéknek
    return mean, eigenfaces, w, threshold
    
