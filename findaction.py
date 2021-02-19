import cv2 as cv
import numpy as np

img_action = cv.imread('./PUBG/imgdata/screendata/action.png', cv.IMREAD_GRAYSCALE)
action_F = cv.imread('./PUBG/imgdata/screendata/actionF.png', cv.IMREAD_GRAYSCALE)
img_F = cv.imread('./PUBG/imgdata/screendata/itemF.png', cv.IMREAD_GRAYSCALE)
def findaction(img) :
    if not findF(img) :
        return 0
    img[520:540,960:980] = 0
    img = img[500:540,960:1000]
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 230, 255, cv.THRESH_TOZERO)
    if np.sum(img_gry) > 100000 :
        return 0
    before = np.sum(255+img_gry)
    after = np.sum(255+img_gry-img_action)
    score = int(before)- int(after)
    if(score<15000) :
        return 1
    else : 
        return 0

def findF(img) :
    img = img[610:640,1072:1102]
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 200, 255, cv.THRESH_TOZERO)
    res = cv.matchTemplate(img_gry,action_F, cv.TM_SQDIFF_NORMED)
    if res<0.3 :
        return True
    else :
        return False
    

def findinter(img) :
    img = img[610:640,1072:1102]
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 200, 255, cv.THRESH_TOZERO)
    res = cv.matchTemplate(img_gry,img_F, cv.TM_SQDIFF_NORMED)

    if res< 0.3 :
        return True
    else :
        return False


def findthrow(img) :
    img = img[990:1020,940:980]
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 200, 255, cv.THRESH_TOZERO)

    if np.sum(img_gry) > 5000 :
        return True
    else :
        return False

# findaction(1)