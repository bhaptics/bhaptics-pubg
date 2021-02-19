import cv2 as cv
import numpy as np
import sys
import screenshot as screen

skipper = True
kill_thresh = 65000
def findkill(pimg) :
    global skipper
    img = pimg[750:790,930:1000]
    img = img[:, :, ::-1]
    
    img = (570+img[:,:,2]-img[:,:,0]-img[:,:,1])/670
    __, img_gry = cv.threshold(img, 1, 255, cv.THRESH_BINARY)
    killval = np.sum(img_gry)
    if killval > kill_thresh and skipper and isblood(img_gry) and iskill(pimg):
        skipper = False
        return 1
    elif killval < kill_thresh/2 :
        skipper = True
    return 0

def isblood(img_gry) :
    img_arr = np.sum(img_gry, axis = 0)
    iszero = -1
    for i in range(len(img_arr)) :
        if img_arr[i]!=0 and iszero == -1 :
            continue
        if img_arr[i]==0 and iszero == -1 :
            iszero = i
            continue
        if img_arr[i]!=0 and iszero != -1 :
            return True
    return False

def iskill(img) :
    img = img[720:740,930:1000]
    __, img_gry = cv.threshold(img, 200, 255, cv.THRESH_BINARY)

    if np.sum(img_gry) > 70000 :
        return True
    else :
        return False

if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize)
    screen.init_screenshot()
    
    findkill(screen.screenshottaker())