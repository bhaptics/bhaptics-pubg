import cv2 as cv
import numpy as np
import findfalling as fall

firstshot = -10
preval = 0
fc = 0
def findfire(img) :
    global preval, fc, firstshot
    if (not fall.isground2(img)) and (not fall.isground(1,img)) :
        return 0



    value = bullet_num(img) 
    if not isgun(img) :
        if value <= 0:
            return 2
        else :
            return 3
    # if value == -2 :
    #     preval = value
    #     return 0
    # print("fire", value, preval)
    if(value == preval):
        return 0
    else :
        # print("fire",fc)
        fc += 1
        preval = value
        firstshot = -10
        return 1
def reset_bullet(img) :
    global preval
    preval = bullet_num(img)

def findaim(img) :
    if (not fall.isground2(img)) and (not fall.isground(1,img)) :
        return 0
    if isgun(img) :
        return 1
    else :
        return 0

def isgun(img) :
    img = img[990:1022,900:930] 
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 200, 255, cv.THRESH_TOZERO)
    value = np.sum(img_gry)
    if value < 4500 :
        return 0
    else :
        return value

reload_stack = 0
def reload(img) : 
    global preval, reload_stack, firstshot
    if reload_stack == 150 :
        reload_stack = 0
        return -1
    reload_stack += 1

    if not isgun(img) or reload_stack<10:
        return 0
    if reload_stack == 30 :
        reset_bullet(img) 
        return 0

    value = bullet_num(img) 
    tempval = preval

    # print("reload val : ", value)
    if(value>tempval ) :
        reload_stack = 100
        if firstshot > value:
            # print(firstshot, value)
            return 0
        firstshot = value
        preval = value
        return 1
    else : 
        return 0

def bullet_sum(img) :
    # imgdir = "./PUBG/testimg/task12/fire6.png"
    # img = cv.imread(imgdir)
    img = img[988:1022,940:980] 
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 200, 255, cv.THRESH_TOZERO)
    # cv.imshow('fall', img_gry)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    return np.sum(img_gry)
    



img_num = []
def init_image() :
    for i in range(10) :
        img_num.append(cv.imread('./PUBG/imgdata/firenum/'+str(i)+'.png', cv.IMREAD_GRAYSCALE))

def bullet_num(img) :
    img = img[988:1025,935:980] 
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 180, 255, cv.THRESH_TOZERO)
    img_arr = np.sum(img_gry, axis = 0)
    if np.sum(img_arr) == 0 :
        return -2
    img_part = []
    iszero = -1
    for i in range(len(img_arr)) :
        if img_arr[i]==0 and iszero == -1 :
            continue
        if img_arr[i]!=0 and iszero == -1 :
            iszero = i
            continue
        if img_arr[i]==0 and iszero != -1 :
            img_part.append(img_gry[:,iszero:i])
            iszero = -1

    img_part.reverse()
    dig = [0, 0, 0]
    counter = 0
    for j in range (len(img_part)) :
        temp = 0.9
        imgsize = np.shape(img_part[j])[1]
        for i in range (10) :
            if(np.shape(img_num[i])[1]<=imgsize) :
                res = cv.matchTemplate(img_part[j], img_num[i], cv.TM_SQDIFF_NORMED)
                if(temp>np.min(res)) :
                    temp = np.min(res)
                    dig[counter] = i
        if(temp != 0.9) :
            counter+=1
        if(counter == 3) :
            break
            
    ret = dig[2]*100+dig[1]*10+dig[0]
    return ret

# init_image()
# newfire(1)