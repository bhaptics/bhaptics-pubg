import cv2 as cv
import numpy as np
import findfalling as fall
import getHP as hp

def isgame(img) :
    if findpeople(img):
        # print("in game")
        return True
    else :
        # print("not game")
        return False


def ispregame(img) :
    if pregame(img) :
        return True
    else :
        return False

    


def pregame(img) :
    img = img[620:650, 850:1070]
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 230, 255, cv.THRESH_TOZERO)
    if 150000<np.sum(img_gry)<250000 :
        return True
    else :
        return False
    


def findpeople(img) :
    numimg = img[35:65, 1770:1800]
    numimg_gry = cv.cvtColor(numimg, cv.COLOR_BGR2GRAY)
    __, numimg_gry = cv.threshold(numimg_gry, 180, 255, cv.THRESH_TOZERO)

    pimg = img[35:65, 1810:1880]
    pimg_gry = cv.cvtColor(pimg, cv.COLOR_BGR2GRAY)
    __, pimg_gry = cv.threshold(pimg_gry, 220, 255, cv.THRESH_TOZERO)
    
    if np.sum(numimg_gry)>10000 and np.sum(pimg_gry)<=np.sum(numimg_gry):
        return True
    else :
        return False


def findpractice(img) :
    numimg = img[35:65, 1590:1670]
    numimg_gry = cv.cvtColor(numimg, cv.COLOR_BGR2GRAY)
    __, numimg_gry = cv.threshold(numimg_gry, 200, 255, cv.THRESH_TOZERO)

    pimg = img[35:65, 1675:1720]
    pimg_gry = cv.cvtColor(pimg, cv.COLOR_BGR2GRAY)
    __, pimg_gry = cv.threshold(pimg_gry, 220, 255, cv.THRESH_TOZERO)
    if np.sum(numimg_gry)>50000 and np.sum(pimg_gry)<=np.sum(numimg_gry):
        return True
    else :
        return False
