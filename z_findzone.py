import cv2 as cv
import numpy as np

def findzone(img) :
    
    # imgdir = "./PUBG/imgdata/task8/blue3.png"
    # img = cv.imread(imgdir)
    img = img[780:785,1620:1900]
    img = 512+img[:,:,2]-img[:,:,0]-img[:,:,1]
    __, img_gry = cv.threshold(img, 530, 255, cv.THRESH_BINARY)
    # cv.imshow('fall', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    zoneval = np.sum(img_gry)
    print(zoneval)
    if(zoneval > 2000 and zoneval<4000) :
        return 1
    return 0

# findzone(1)