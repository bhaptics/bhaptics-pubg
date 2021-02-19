import cv2 as cv
import numpy as np
import findfalling as fall
import findfire as fire

wepslot = 0
prev = [0, 0]
weptick = 0
x_slot = 0
def getwepnum(img, num) :
    global wepslot, prev, weptick, x_slot
    if num == wepslot :
        return -1
    # if wepslot == -1 :
    #     wepslot = num
    #     return num
    guntype = fire.isgun(img)
    bullet = fire.bullet_sum(img)
    if weptick == 0 :
        prev[0] = guntype
        prev[1] = bullet
        weptick += 1
    # print(guntype, bullet, prev, weptick)

    if not prev[0]*0.9<=guntype<=prev[0]*1.1 or\
        not prev[1]*0.9<=bullet<=prev[1]*1.1 :
        # print(wepslot, "to", num)
        if num == 7 :
            if x_slot == 0 :
                x_slot = wepslot
                wepslot = 0
                ret = x_slot*10
            else :
                wepslot = x_slot
                x_slot = 0
                ret = wepslot
        else :
            ret = wepslot*10 + num        
            wepslot = num
            x_slot = 0
        prev[0] = guntype
        prev[1] = bullet
        weptick = 0
        return ret
    else :
        weptick += 1
        if weptick == 40 :
            weptick = 0
            return -1
        return 0

# getwepnum(1)
