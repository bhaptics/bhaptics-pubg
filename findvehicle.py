import cv2 as cv
import numpy as np
import findfalling as fall

vehicles = ["buggy", "dacia", "dirtbike", "minibus", "mirado",\
    "motorbike", "pickuptruck", "tuk", "uaz", "zima", "scooter", "boat"]


img_vehicles_templ = []
def init_image() :
    for i in range(len(vehicles)) :
        img_vehicles_templ.append(cv.imread('./PUBG/imgdata/vehicle/'+vehicles[i]+'.png', cv.IMREAD_GRAYSCALE))


whatv = ""
def findvehicle(img) :
    global whatv
    # imgdir = "./PUBG/testimg/err/squad2.png"
    # img = cv.imread(imgdir)
    img_gas = img[1020:1040,283:300]
    img_gas = cv.cvtColor(img_gas, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gas, 200, 255, cv.THRESH_TOZERO)

    img_gas2 = img[1020:1040,540:557]
    img_gas2 = cv.cvtColor(img_gas2, cv.COLOR_BGR2GRAY)
    __, img_gry2 = cv.threshold(img_gas2, 200, 255, cv.THRESH_TOZERO)

    img_gas_templ =  cv.imread("./PUBG/imgdata/screendata/gas.png", cv.IMREAD_GRAYSCALE)

    res = cv.matchTemplate(img_gry,img_gas_templ, cv.TM_SQDIFF_NORMED)
    res2 = cv.matchTemplate(img_gry2,img_gas_templ, cv.TM_SQDIFF_NORMED)

    
    if res<0.5 :
        return findspeed(img)
    elif res2<0.5 :
        return findspeed(img, 257)
    else :
        return 0


    # if(res>0.5 and res2>0.5) :
    #     print("not vehicle",res)
    #     whatv = ""
    #     return 0

    # else :
    #     if(not whatv) :
    #         whatv = whatvehicle(img)
    #     print(whatv, end=' ')
    #     return findspeed(img)


def whatvehicle(img) :
    global vehicles, img_vehicles_templ
    img_vehicle = img[930:1060,40:90]
    img_vehicle = cv.cvtColor(img_vehicle, cv.COLOR_BGR2GRAY)
    __, img_vehicle = cv.threshold(img_vehicle, 200, 255, cv.THRESH_TOZERO)
    arr_vehicle = [1, 0]
    for i in range(len(vehicles)) :
        temp = cv.matchTemplate(img_vehicle, img_vehicles_templ[i], cv.TM_SQDIFF_NORMED)
        if(arr_vehicle[0]>temp) :
            arr_vehicle[0] = temp
            arr_vehicle[1] = i
    return vehicles[arr_vehicle[1]]

def imgextract(name) :
    imgdir = "./PUBG/imgdata/task4/"+name+".png"
    img = cv.imread(imgdir)
    img = img[930:1060,40:90]
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 200, 255, cv.THRESH_TOZERO)
    cv.imwrite("./PUBG/imgdata/vehicle/"+name+".png", img_gry)

def findspeed(img, squad = 0) :
    # imgdir = "./PUBG/imgdata/task4/motorbike2.png"
    # img = cv.imread(imgdir)
    img = img[975:1020, 140+squad:200+squad]
    img_gry = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    __, img_gry = cv.threshold(img_gry, 200, 255, cv.THRESH_TOZERO)
    img_gry = cv.resize(img_gry, (40,30), interpolation=cv.INTER_AREA)

    # print(squad)
    dig = [0, 0, 0]

    for j in range (3) :
        temp = 1
        for i in range (10) :
            res = cv.matchTemplate(img_gry[:,1+j*13:14+j*13],fall.img_num[i], cv.TM_SQDIFF_NORMED)
            if(temp>np.min(res)) :
                temp = np.min(res)
                dig[j] = i

    # print( dig[0]*100+dig[1]*10+dig[2],"km/h")
    return dig[0]*100+dig[1]*10+dig[2]
# init_image()
# for i in vehicles :
#     imgextract(i)
# fall.init_image()
# findvehicle(1)
# findspeed(1)