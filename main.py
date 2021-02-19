import screenshot as screen
import findfalling as fall
import findplane as plane
import getHP as hp
import findkill as kill
import findvehicle as vh
import findaction as act
import findfire as fire
import findweapon as wp
import time
import cv2 as cv
import numpy as np
import haptics 
import isgame
import GUI
import sys
from threading import Thread
from pynput import keyboard, mouse

l_clicked = 0
reloaded = False
swapped = 0
throw = False 

def on_click(x, y, button, pressed):
    if not listenerON :
        return -1
    th1 = Thread(target=clickfunc, args=(button, pressed))
    th1.setDaemon(True)
    th1.start()

def on_scroll(x, y, dx, dy) :
    global swapped
    if not listenerON :
        return -1
    swapped = 6

def clickfunc(button, pressed) :
    global l_clicked, reloaded, throw
    if button == mouse.Button.left:
        time.sleep(0.1)
        if(pressed) :
            temp = fire.findfire(img)
            if gamestat == PREGAME : 
                if temp == 2 :
                    haptics.punch()
                else :
                    throw = True
                return 0

            if temp == 1 :
                haptics.fire()
                if reloaded == True and fire.reload_stack>10 :
                    reloaded = False
                    fire.reload_stack = 0
            elif temp == 2 :
                haptics.punch()
            elif temp == 3 :
                throw = True
            

            l_clicked = 1
        else :
            # print("unpressed")
            if throw :
                haptics.throw()
                throw = False
            l_clicked = 0
    
    elif button == mouse.Button.right:
        temp = fire.findaim(img)
        if pressed and temp == 1 :
            haptics.aim()

def keyfunc(key_char) :
    global reloaded, swapped
    if key_char == 'r' or key_char == 'R' :
        fire.reload_stack = 0
        reloaded = True
    elif key_char == '1' or key_char == '!':
        swapped = 1
    elif key_char == '2' or key_char == '@':
        swapped = 2
    elif key_char == '3' or key_char == '#':
        swapped = 3
    elif key_char == '4' or key_char == '$':
        swapped = 4
    elif key_char == '5' or key_char == '%':
        swapped = 5
    elif key_char == 'x' or key_char == 'X':
        swapped = 7
    elif key_char == 'f' or key_char == 'F' :
        if act.findinter(img) :
            haptics.interact()


def on_press(key) :
    ckey = str(key)
    key_char = ckey[1]
    if not listenerON :
        return -1
    th2 = Thread(target=keyfunc, args=(key_char,))
    th2.setDaemon(True)
    th2.start()

practice_fall = False
def stream(img) :
    global l_clicked, reloaded, swapped, practice_fall

    hap = [0, # 0 Damaged
            0, # 1 Kill
            0, # 2 Fire
            0, # 3 Run
            0, # 4 Impact
            0, # 5 Action
            0, # 6 Blue Zone
            0, # 7 Vehicle
            0, # 8 Reload
            0, # 9 Swap
            0, # 10 Aim
            0] # 11 Low HP
    dam = 0
    shot = 0
    life = hp.getHP(img)
    # print("HP : ", life)
    if gamestat == INGAME :
        if 1<=life<=15 :
            hap[11] = 1

        if life <= 0 and  hp.isdead(img) :
            haptics.active(4, True)
            haptics.logger.info("game end")
            return -1

        hap[1] = kill.findkill(img)
    
    if gamestat == PRACTICE :
        if not practice_fall and fall.isfalling(img) :
            practice_fall = True
        if practice_fall and fallandpara(img) :
            practice_fall = False



    if not act.findaction(img) :
        dam = hp.damage(life)
        if 0< dam < 7 and gamestat == INGAME:
            hap[6] = 1
        elif dam >= 7 and gamestat != PREGAME:
            hap[0] = dam
    else :
        hap[5] = 1
        
    if swapped == 6:
        if fall.isground2(img) or fall.isground(1,img) :
            hap[9] = 100
        swapped = 0
        wp.wepslot = 0
        reloaded = False
    elif swapped :
        temp = wp.getwepnum(img, swapped)
        if temp == -1:
            swapped = 0
        else :
            l_clicked = 0 
            
        if temp >= 1 :
            hap[9] = temp
            swapped = 0
            reloaded = False
            fire.reload_stack = 0
            fire.firstshot = -10

    if reloaded :
        temp_reload = fire.reload(img)
        if temp_reload == 1 :
            hap[8] = 1
        elif temp_reload == -1:
            reloaded = False 

    if l_clicked == 1:
        l_clicked = 2
    elif l_clicked == 2 :
        shot = fire.findfire(img)
        if shot == 1 :
            hap[2] = shot
            if fire.reload_stack > 100 :
                fire.reload_stack = 0
                reloaded = False

    hap[7] = vh.findvehicle(img)
    haptics.ingame(hap)
    return 0


def airplane(img) :
    status = plane.findplane(img)
    if(status == -1) :
        if fall.isfalling(img) :
            return 2
        else :
            return -1
    # exp.getthresh()
    haptics.airplane()
    return 1

def fallandpara(img) :
    speed = fall.findfalling(img)
    status = fall.falltype(speed)


    haptics.fall(status)

    if(speed==-2) :
        haptics.landing()
        fall.status = 0
        fall.prespeed = 100
        return True
    return False

fallsys = 0
def airflow(img) :
    global fallsys
    # In airplane
    if fallsys == 0 :
        if airplane(img) == 2:
            fallsys = 1
    # Falling & Parachute
    elif fallsys == 1 :
        if fallandpara(img) :
            fallsys = 0
            return False
    time.sleep(0.1)
    return True


PREGAME = 0
INGAME = 1
PRACTICE = 2
INAIR = 3

gamestat = PREGAME
listenerON = False
notgame = 31
frame = True
TYPE_TRESH=30
changestack = TYPE_TRESH
def changestat(gtype) :
    global gamestat, changestack
    if changestack < TYPE_TRESH :
        changestack +=1 
        return 0
    if gtype == gamestat and notgame == 0:
        changestack = 0
        return 0

    gamestat = gtype
    stat_text = ""
    if gtype == 0 :
        stat_text = "PREGAME"
    elif gtype == 1 :
        stat_text = "INGAME"
    elif gtype == 2 :
        stat_text = "PRACTICE"
    elif gtype == 3 :
        stat_text = "INAIR"

    msg = "changed state : " + stat_text
    haptics.logger.info(msg)
    GUI.state_change(stat_text)
    changestack = 0 

frame = True 
img = None   
tttt= 0
def mainflow() :
    global gamestat, listenerON, notgame, changestack, img, frame,tttt

    start = 0
    haptics.logger.info("init finish")
    while(not GUI.isexit) :
        # print(time.time() - tttt)
        # tttt= time.time()
        if not frame :
            time.sleep(0.02)
        img = screen.screenshottaker()    
        # cv.imshow('fall',img)
        # cv.waitKey(0)
        # cv.destroyAllWindows()   
        # print(np.shape(img))
        frame = False
        ans = isgame.isgame(img)
        if not ans :
            listenerON = False
            if notgame == 30 :
                haptics.logger.info("not game")
                GUI.state_change("not game")
                changestack = TYPE_TRESH
            if notgame <= 30 :
               notgame += 1
            continue

        if notgame > 30: 
            changestack = TYPE_TRESH
            if isgame.ispregame(img) :
                changestat(PREGAME)
            else :
                changestat(gamestat)
        notgame = 0

        if gamestat != INAIR :
            listenerON = True
        
        if airplane(img) == 1 and gamestat != INAIR:
            changestack = TYPE_TRESH
            changestat(INAIR)
            listenerON = False

        if gamestat == INAIR :
            if not airflow(img) :
                changestack = TYPE_TRESH
                changestat(INGAME)
                listenerON = True
        else :
            if isgame.ispregame(img) :
                changestat(PREGAME)
            else :
                if isgame.findpractice(img) :
                    changestat(PRACTICE)
                else :
                    changestat(INGAME)

        if gamestat == INGAME or gamestat == PRACTICE or gamestat == PREGAME:
            if stream(img) == -1 :
                changestack = TYPE_TRESH
                changestat(PREGAME)
                changestack = -100
    haptics.logger.info("main flow exit")

def timer() :
    global frame
    while(not GUI.isexit) :
        time.sleep(0.05)
        frame = True

def main() :
    mouse_listener = mouse.Listener(on_click=on_click, on_scroll = on_scroll) 
    key_listener = keyboard.Listener(on_press = on_press)
    mouse_listener.start()
    key_listener.start()

    haptics.init_haptic()
    fall.init_image()
    vh.init_image()
    fire.init_image()
    screen.init_screenshot()

    th3 = Thread(target=mainflow, args=())
    th3.setDaemon(True)
    th3.start()

    
    th4 = Thread(target=timer, args=())
    th4.setDaemon(True)
    th4.start()

    GUI.setGUI()
    
    mouse_listener.stop()
    key_listener.stop()
    haptics.logger.info("main exit")

if __name__ == "__main__":
    main()
sys.exit()



