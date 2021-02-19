import cv2 as cv
import numpy as np

def findplane(img) :

    # imgdir = "./PUBG/testimg/err/squad.png"
    # img = cv.imread(imgdir)
    img_plane = cv.imread('./PUBG/imgdata/screendata/plane.png', cv.IMREAD_GRAYSCALE)
    img1 = img[790:1080,70:150]
    img2 = img[790:1080,325:405]
    img_gry = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    img_gry2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    img_gry[44:217, 25:53] = 0
    img_gry2[44:217, 25:53] = 0
    __, img_gry = cv.threshold(img_gry, 200, 255, cv.THRESH_TOZERO)
    __, img_gry2 = cv.threshold(img_gry2, 200, 255, cv.THRESH_TOZERO)
    
    # cv.imshow('fall', img_gry2)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    # print(np.shape(img_gry), np.shape(img_plane))
    res = cv.matchTemplate(img_gry,img_plane, cv.TM_SQDIFF_NORMED)
    res = np.min(res)
    res2 = cv.matchTemplate(img_gry2,img_plane, cv.TM_SQDIFF_NORMED)
    res2 = np.min(res2)
    # print(res2)
    if(res<0.85 or res2<0.85) :
        return 1
    else :
        # print("Not Plane")
        return -1



# findplane(1)