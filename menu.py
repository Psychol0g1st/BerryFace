from time import sleep
from gpiozero import Button, LED
import Adafruit_SSD1306
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

def InitMenu():
    #deklarálja a gombok, képenyő és más változókat
    global button_1
    global button_2
    global button_3
    global disp
    global draw
    global font
    global message
    
    #Inicializálja a gombokat
    btn_1 = 16 #pin
    btn_2 = 20 #pin
    btn_3 = 21 #pin
    button_1 = Button(btn_1)#Piros
    button_2 = Button(btn_2)#Kék
    button_3 = Button(btn_3)#Zöld
    #inicializálja OLED kijelzőt
    RST = 0
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
    disp.begin()
    disp.clear()
    disp.display()
    #OLED paraméterei
    #A képernyő képet jeleníti meg, a továbbiakban úgyis kezelem az üzenet megjelenítését
    message = Image.new('1', (disp.width, disp.height)) #üzenet változó
    draw = ImageDraw.Draw(message) #üzenet "rajzolása" a változóba
    font = ImageFont.truetype("/home/pi/Desktop/FaceRec/BerryFace/Data/fonts/joystix_monospace.ttf", 10)#betűstílus valasztás
    disp.clear() #kijelző tisztítás
    draw.rectangle((0,0,disp.width,disp.height), outline=0, fill=0) #üzenet háttér rajzolása
    disp.image(message) #üzenet behelyezése a képernyő memóriába
    disp.display() #üzenet megjelenítése
def ShowMessage(text): #egyszerű üzenet
    disp.clear()
    draw.rectangle((0,0,disp.width,disp.height), outline=0, fill=0)
    (font_width, font_height) = font.getsize(text)
    draw.text((disp.width//2 - font_width//2, disp.height//2 - font_height),text, font=font, fill=255)#szöveg "rajzolása" a képernyőre
    message.paste(message.rotate(180))#kép forgatása 180 fokra
    disp.image(message)
    disp.display()
def ShowSlidingMessage(text): #futó üzenet
    step = 10
    disp.clear()
    draw.rectangle((0,0,disp.width, disp.height), outline=0, fill=0)
    (font_width, font_height) = font.getsize(text)
    for x in range(disp.width//step + font_width//step):
        draw.text((disp.width-x*step, disp.height//2 - font_height),text, font=font, fill=255)
        message.paste(message.rotate(180))
        disp.image(message)
        disp.display()
        sleep(0.1)
        disp.clear()
        draw.rectangle((0,0,disp.width,disp.height), outline=0, fill=0)
        
def Blinking(text, mode):#pislogó üzenet
    disp.clear()
    draw.rectangle((0,0,disp.width, disp.height), outline=0, fill=0)
    (text_width, text_height) = font.getsize(text)
    stop = False
    if mode == 1: #ameddig nem nyomjuk meg a  gombot
        while not button_3.is_pressed:
            draw.rectangle((0,0,disp.width,disp.height), outline=0, fill=0)
            draw.text((disp.width//2 - text_width//2, disp.height//2 - text_height),text, font=font, fill=255)
            message.paste(message.rotate(180))
            disp.image(message)
            disp.display()  
            if button_1.is_pressed:
                return 2
            disp.clear()
            disp.display()
        return 1
    else:
        disp.clear()
        disp.display()
        sleep(0.2)
        draw.rectangle((0,0,disp.width,disp.height), outline=0, fill=0)
        draw.text((disp.width//2 - text_width//2, disp.height//2 - text_height),text, font=font, fill=255)
        message.paste(message.rotate(180))
        disp.image(message)
        disp.display()  
        
        
    
    
def MenuHandler(menu, menu_points):#menű kezelő függvény
    current_menu = menu
    select = False
    ShowMessage(menu_points[current_menu])
    while not select: #Green
        if button_2.is_pressed: #blue
            current_menu += 1
            if current_menu > len(menu_points)-1:
                current_menu = 0
            ShowMessage(menu_points[current_menu])
        elif button_3.is_pressed:
             select = True   
        sleep(0.1)
    if select:
        return current_menu
    else:
        ShowSlidingMessage("Menu valasz. hiba")
def DeleteUserMenu(users_file_path,id_list,name_list):#Felhasználó kiválasztása törlés esetében
    user = 0
    select = 0
    ShowMessage(name_list[user])
    while True:
        if button_2.is_pressed:
            user += 1
            if user > len(name_list)-1:
                user = 0
            ShowMessage(name_list[user])
        elif button_3.is_pressed:
            select = 3
            break
        elif button_1.is_pressed:
            select = 1
            break
        sleep(0.1)
    if select == 3:
        return user
    if select == 1:
        return -1
def Close():
    if button_1.is_pressed:
       return True
    else:
        return False
def ShutdownMenu():
    disp.command(Adafruit_SSD1306.SSD1306_DISPLAYOFF)
    
    