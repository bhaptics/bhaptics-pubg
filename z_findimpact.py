import screenshot as screen
import cv2 as cv
import numpy as np
import math

def finddir(img) :

    # imgdir = "./PUBG/imgdata/task9/fall2.png"
    # img = cv.imread(imgdir)
    img = img[40:55,800:1160]
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, img_gry = cv.threshold(img_gry, 220, 255, cv.THRESH_TOZERO)
    
    # cv.imshow('fall', img_gry)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    dir_arr = np.sum(img_gry, axis = 0)

    temp = []
    for i in range(len(dir_arr)) :
        if(dir_arr[i]>2000) :
            temp.append(i)

    dir_pixel = []
    prev = 0
    for i in range(len(temp)) :
        if(temp[i]<20 or temp[i]>340 or prev+10>temp[i]) :
            continue
        dir_pixel.append(temp[i])
        prev = temp[i]
    
    if(len(dir_pixel) == 0) :
        return -1

    return dir_pixel[math.floor(len(dir_pixel)/2)]


prev_dir = 0
impact_stack = [0, 0]
prev_mouse = [0, 0]
def findimpact(dir_pixel, mouse) :
    global prev_mouse, prev_dir, impact_stack
    dir_delta = dir_pixel - prev_dir
    if(dir_delta>0) :
        impact_stack[0] += dir_delta
    else :
        impact_stack[1] -= dir_delta
    prev_dir = dir_pixel


    # print(impact_stack, dir_delta)

    if dir_delta == 0 \
        or (impact_stack[0]>15 or impact_stack[1]>15) \
        or (dir_delta>0 and impact_stack[1] != 0)   :
        reset_stack()



    if 7<(impact_stack[0]+impact_stack[1])<25\
         and abs(impact_stack[0]-impact_stack[1])<10\
         and impact_stack[0] >= 1 and impact_stack[1] >= 1 :

        print("impact", impact_stack)
        reset_stack()
        return 1

    prev_mouse[1] = mouse - prev_mouse[0]
    prev_mouse[0] = mouse
    return 0

def reset_stack() :
    global frame_counter, impact_stack
    frame_counter = 0
    impact_stack = [0, 0]

# while(True) :
#     img = screen.screenshottaker()
#     direction = finddir(img)
#     # print(direction)
#     findimpact(direction, screen.mouse_x())