import cv2 as cv
import numpy as np
import sys


preHP = 100
counter = 0
def getHP(img) :

    # imgdir = "./PUBG/testimg/err/hp.png"
    # img = cv.imread(imgdir)
    global preHP, counter
    img = img[1032:1045,753:1167]
    # img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # ret, img_gry = cv.threshold(img_gry, 230, 255, cv.THRESH_TOZERO)

    # sobel = np.array([[1, 0, -1]])
    # img_gry = cv.filter2D(img_gry, -1, sobel)
    # ret, img_gry = cv.threshold(img_gry, 230, 255, cv.THRESH_TOZERO)
    # cv.imshow('fall', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    hparr = np.sum(img, axis = 0)
    # hparr = np.sum(hparr, axis = 1)
    # if hparr[1]<1000 :
    #     return -1
    for j in range(3) :
        if(hparr[0][j]*0.9<hparr[1][j]<hparr[0][j]*1.1) :
            return -1

    # if(hparr[1]<1500 or 0.9*hparr[0]<hparr[1]<1.1*hparr[0]) :
    #     hparr = np.max(img_gry, axis = 0) - np.min(img_gry, axis = 0)
    #     print(hparr)
    #     return redHP(hparr)

    for i in range(2,len(hparr)) :
        for j in range(3) :
            if(not hparr[i-1][j]*0.9<hparr[i][j]<hparr[i-1][j]*1.1) :
                if i == 2 :
                    return -1
                nowHP = i/413*100
                if (nowHP>15  or preHP<nowHP or round(nowHP) == 0) and counter<5 : # 이거 필요없을지도? ㄴㄴ 필요함
                    counter += 1
                    return preHP
                else :
                    counter = 0
                    return nowHP
    return -1



dam_stack = 0
def damage(life) :
    global dam_stack, preHP
    if(life == -1 or life == 0) :
        return 0
    if dam_stack<-1 :
        dam_stack = 0
    dam = preHP-life
    preHP = life
    dam_stack += dam
    if(dam>=0.8 or dam_stack>1) :
        # print("HP -",dam)
        dam_stack = 0
        return dam
    else :
        return 0

def isdead(img) :   
    img = img[940:970,760:900]
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 230, 255, cv.THRESH_TOZERO)
    # cv.imshow('fall', img_gry)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    # print(np.sum(img_gry))
    if(np.sum(img_gry)>100000) :
        return True
    else :
        return False

# np.set_printoptions(threshold=sys.maxsize)
# imgdir = "./PUBG/testimg/task9/fall1.png"
# img = cv.imread(imgdir)
# getHP(img)