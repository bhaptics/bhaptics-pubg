import cv2 as cv
import numpy as np

on_shape = False
same_size = False
cut=[0,0,0,0]
def init_convert(img) :
    global on_shape, same_size
    size = np.shape(img)
    y = size[0]
    nx = size[1]
    x = y*16/9
    dx = nx-x

    if(dx == 0) :
        same_shape = True
    elif dx>0 :
        cut[0] = int(x/5)
        cut[1] = int(x/5 + dx/2)
        cut[2] = int(nx-x/5 - dx/2)
        cut[3] = int(nx-x/5)
    else :
        cut[0] = -y
        cut[1] = int(nx/3)
        cut[2] = int(nx/3*2)
        cut[3] = int(-dx/2)
    if(y == 1080) :
        same_size = True
    


def imgconvert(img) :
    # imgdir = "./PUBG/imgdata/task13/big9.png"
    # img = cv.imread(imgdir)
    if on_shape and same_size :
        return img

    if not on_shape and cut[0] >= 0:
        newimg = np.hstack([img[:,:cut[0],:],img[:,cut[1]:cut[2],:]])
        newimg = np.hstack([newimg, img[:,cut[3]:,:]])

    elif not on_shape and cut[0] < 0:
        padimg = np.zeros((-cut[0], cut[3], 3), dtype=np.uint8)
        newimg = np.hstack([img[:,:cut[1],:],padimg])
        newimg = np.hstack([newimg, img[:,cut[1]:cut[2],:]])
        newimg = np.hstack([newimg, padimg])
        newimg = np.hstack([newimg, img[:,cut[2]:,:]])


    if not same_size :
        newimg = cv.resize(newimg, (1920, 1080), interpolation=cv.INTER_CUBIC)

    # cv.imshow('fall', newimg)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    # cv.imwrite("./PUBG/imgdata/task13/small.png", newimg)
    return newimg

def imgcvtthresh(img, thr) :
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, thr, 255, cv.THRESH_TOZERO)
    return img_gry



def tttt(imgdir) :
    imgdir = "./PUBG/testimg/err/bigerr.png"
    img = cv.imread(imgdir)
    init_convert(img)
    print(cut)
    img = imgconvert(img)
    cv.imwrite("./PUBG/testimg/err/big2.png", img)

# tttt(1)