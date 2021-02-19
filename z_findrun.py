import cv2 as cv
import numpy as np


premap = [[[None]]]
runstack = 0
def isrun(img) :
    global premap, runstack
    
    if runstack == 10 :
        runstack = 0
        return -1
    runstack += 1
    thismap = img[850:950, 1700:1800]

    # cv.imshow('fall',thismap)
    # cv.waitKey(0)
    # cv.destroyAllWindows()   

    if premap[0][0][0] == None :
        premap = img[840:960, 1690:1810]

    res = cv.matchTemplate(premap,thismap, cv.TM_SQDIFF_NORMED)
    n1 = np.argmin(res)
    n2 = n1%21 - 10
    n1 = n1//21 - 10
    print(n1, n2)
    premap = img[840:960, 1690:1810]
    if 0<abs(n1)+abs(n2)<4 :
        runstack = 0
        return 1
    elif abs(n1)+abs(n2)>=4 :
        runstack = 0
        return -1
    else :
        return 0 


# imgdir = "./PUBG/testimg/err/error2.png"
# img = cv.imread(imgdir)
# isrun(img)
# imgdir = "./PUBG/testimg/task8/blue2.png"
# img = cv.imread(imgdir)
# isrun(img)