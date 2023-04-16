#importálok minden függvényt menu.py, face_recognition.py, face_registration.py, init.py fájlokból
from menu import *
from face_recognition import *
from face_registration import *
from calculation import *
from init import *
from time import sleep
from subprocess import call


#A mappák eleresi utja
original_img_path = "/home/pi/Desktop/FaceRec/BerryFace/Faces/original/"
cropped_img_path = "/home/pi/Desktop/FaceRec/BerryFace/Faces/cropped/"
unknown_img_path = "/home/pi/Desktop/FaceRec/BerryFace/Faces/unknown/"
cascade_path = "/home/pi/Desktop/FaceRec/BerryFace/Data/Haarcascades/haarcascade_frontalface_default.xml"
id_file = "/home/pi/Desktop/FaceRec/BerryFace/Data/id_increment.txt"
users_file_path = "/home/pi/Desktop/FaceRec/BerryFace/Data/users.txt"
data_path = "/home/pi/Desktop/FaceRec/BerryFace/Data/"

#A változók deklarálása
img_num, file_names = GetImageNum(cropped_img_path) #(init.py)függveny megszámolja a mappába lévő fájlok darabszámát
reg_img_num = 10 #A regisztláló képek száma
principal_component_num = 30 #PCA komponens száma
original_img_width = 640 #px
original_img_height = 480 #px
cropped_img_width = 100 #px
cropped_img_height = 100 #px
threshold = 0 #kép azonosításának határértéke
menu = 1
menu_points = ["kilépés", "arcfelismerés", "arc regisztráció", "felhasz. tör."] #Menu pontok
Id = SetId(id_file) #(init.py) beállítja az ID a jelenlegi ID szám értékét

#Tömbök deklarálása
calculation_faces = ReadCroppedImgs(cropped_img_path, img_num, cropped_img_width, cropped_img_height)#(init.py) beolvassa a méretezett képeket
mean_face = InitMeanFace(cropped_img_width, cropped_img_height) #(init.py)Átlag arcvektor deklarálása
eigenfaces = [] #Sajátarc vektor römb deklarálása
weights = InitWeights(principal_component_num, img_num)#(init.py)Súly vektortömb deklarálása
InitMenu()#(menu.py)Menű inicializáció, képernyő bekapcsolása
ShowMessage("BerryFace")#(menu.py)üzenet megjeleítése
sleep(2)
ShowMessage("Számolás elvég.")
mean_face, eigenfaces, weights, threshold = Calculation(cropped_img_width, cropped_img_height, principal_component_num, img_num, calculation_faces)#(calculation.py)Kezdő számolások a meglévő képekből
#Fő ciklus, menű vezérlés
while menu != 0:
    menu = MenuHandler(menu, menu_points)#(menu.py) Menűpont választása
    if menu == 1:#Arcfelismerés
        FaceRecognition(img_num, mean_face, eigenfaces, weights, threshold,cascade_path,cropped_img_width, cropped_img_height, unknown_img_path, users_file_path,file_names)
    elif menu == 2:#Arcregisztráció
        status = FaceRegistration(reg_img_num, cascade_path,original_img_path,Id,users_file_path)
        if status:
            ShowSlidingMessage("sikeres regisztráció!")#(menu.py)
            ShowMessage("újraszámolás:")
            Id += 1
            CropImages(img_num, cropped_img_width,cropped_img_height,original_img_path,cropped_img_path, cascade_path,Id)
            img_num,file_names = GetImageNum(cropped_img_path) #csak teszt
            calculation_faces = ReadCroppedImgs(cropped_img_path, img_num, cropped_img_width, cropped_img_height)
            mean_face, eigenfaces, weights, threshold = Calculation(cropped_img_width, cropped_img_height, principal_component_num, img_num, calculation_faces)
        else:
            ShowSlidingMessage("sikertelen regisztráció!")
    elif menu == 3:#Felhasználó rötlése
        id_list = []
        name_list = []
        file = open(users_file_path, 'r')
        for values in file:
            ID, name = values.split(':')[:]
            id_list.append(ID)
            name = name.replace('\n', '')
            name_list.append(name)
        file.close()
        status = DeleteUserMenu(users_file_path,id_list,name_list)#(menu.py) Felhaszáló kiválasztása törlésre
        if status >= 0 :
            user = status
            ShowSlidingMessage("törlöm " + name_list[user] + " felhasználót!")
            original_imgs = os.listdir(original_img_path)
            for img in original_imgs:
                ID = img.split('_')[0]
                if ID == id_list[user]:
                    os.remove(original_img_path+img)
            cropped_imgs = os.listdir(cropped_img_path)
            for img in cropped_imgs:
                ID = img.split('_')[0]
                if ID == id_list[user]:
                    os.remove(cropped_img_path+img)
            file = open(users_file_path,'r')
            temp = open(data_path+"temp.txt",'w')
            for values in file:
                if values.split(':')[0] != id_list[user]:
                    temp.write(values)
            file.close()
            temp.close()
            os.remove(users_file_path)
            os.rename(data_path+"temp.txt", users_file_path)
            ShowSlidingMessage("sikeres törlés!")
            ShowMessage("újraszámolás:")
            img_num,file_names = GetImageNum(cropped_img_path) #csak teszt
            calculation_faces = ReadCroppedImgs(cropped_img_path, img_num, cropped_img_width, cropped_img_height)
            mean_face, eigenfaces, weights, threshold = Calculation(cropped_img_width, cropped_img_height, principal_component_num, img_num, calculation_faces)
        else:
            ShowSlidingMessage("sikertelen törlés!")
ShowMessage("Viszlát!")
SaveId(id_file, Id) #Lementi az ID-t egy fájlba
sleep(3)
ShutdownMenu()#kikapcsolja a képernyőt és a menűt
call("sudo shutdown -h now", shell=True) #kikapcsolja az eszközt
