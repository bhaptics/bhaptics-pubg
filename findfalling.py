import cv2 as cv
import numpy as np


img_num = []
img_kmh = None
def init_image() :
    global img_kmh
    img_kmh = cv.imread('./PUBG/imgdata/screendata/kmh.png', cv.IMREAD_GRAYSCALE)
    for i in range(10) :
        img_num.append(cv.imread('./PUBG/imgdata/numdata/'+str(i)+'.png', cv.IMREAD_GRAYSCALE))


def findfalling(img) :
    img_gry = img[535:565,1420:1505]  #얘네들 비율로 바꿔서 해상도 상관없이 딸수있게
    img_gry = cv.cvtColor(img_gry, cv.COLOR_BGR2GRAY) #사이즈도 이쪽에 맞춰서 convert 해야함
    __, img_gry = cv.threshold(img_gry, 200, 255, cv.THRESH_TOZERO)    


    if isground(img_gry, img) :
        return -2

    img_arr = np.sum(img_gry, axis = 0)
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

    if len(img_part) < 4 :
        return 0
    # for i in img_part :
    img_part.reverse()
    dig = [0, 0, 0]
    counter = 0
    for j in range (4,len(img_part)) :
        temp = 0.9
        imgsize = np.shape(img_part[j])[1]
        for i in range (10) :
            if(np.shape(img_num[i])[1]>=imgsize) :
                res = cv.matchTemplate(img_num[i],img_part[j], cv.TM_SQDIFF_NORMED)
                if(temp>np.min(res)) :
                    temp = np.min(res)
                    dig[counter] = i
        if(temp != 0.9) :
            counter+=1
        if(counter == 3) :
            break
            
    ret = dig[2]*100+dig[1]*10+dig[0]
    print(ret)
    return ret


pre_speed = 100
status = 0
def falltype(speed) :
    global pre_speed, status
    # print(speed," : ", end = '')
    if speed>600 :
        speed-=500
    if(speed==0 or speed>234 or speed<pre_speed*0.15 or speed>pre_speed*6) :
        # print("Skip Data")
        return status

    pre_speed = speed
    next_stack = 0
    if(speed<=126 and status == 0) : #At First Fall
        return 1
    if (speed>126 ) : #FreeFall
        status = 1
    elif(speed<126 and status == 1) : #Parachute Active
        status = 2
    elif status == 2 or status == 3:          #Parachute
        status = 3
    return status

def isfalling(img) :
    global status
    img = img[545:565,1440:1495] 
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 200, 255, cv.THRESH_TOZERO)
    res = cv.matchTemplate(img_gry, img_kmh, cv.TM_SQDIFF_NORMED)


    if np.min(res)<0.3 :
        return True
    else :
        return False



def isground(img_gry, img) :
    # imgdir = "./PUBG/testimg/err/smoke2.png"
    # img = cv.imread(imgdir)
    img_5 = img[750:780, 1615:1720]
    img_gry_5 = cv.cvtColor(img_5, cv.COLOR_BGR2GRAY)
    __, img_gry_5 = cv.threshold(img_gry_5, 200, 255, cv.THRESH_TOZERO) 
    if np.sum(img_gry_5) > 150000 :
        return False

    if np.sum(img_gry) <30000 :
        img = img[795:1051, 1627:1884]
        img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        __, img_gry = cv.threshold(img_gry, 200, 255, cv.THRESH_TOZERO) 
        score = np.sum(img_gry)
        if score > 60000:
            return True
    return False

def isground2(img) :
    img = img[785:793, 1874:1883]
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 220, 255, cv.THRESH_TOZERO)   

    if np.sum(img_gry) > 13000 :
        return True
    return False

if __name__ == "__main__":
    init_image()
    print(isfalling(1))