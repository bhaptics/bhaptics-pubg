from bhaptics import haptic_player as player
from time import sleep
import logging
import GUI

IS_HAPTIC = True
tacts = ["Body_Action", "Body_Airplane", "Body_Bluezone", "None",       #3
     "Body_Damage", "Body_Carstart","Body_Fire","Body_Freefall",            #7
     "Body_Throw", "Body_Kill","Body_Parachute", "Body_Parachute_Active",   #11
    "Body_Landing", "Body_Swapwheel", "Body_Reload", "Body_Aim",            #15
    "Body_Heartbeat", "None", "None", "Body_Punch",             #19
    "None", "None", "None", "Body_Interact",                  #23
    "None", "None", "Body_Swapin1", "Body_Swapin2",           #27
    "Body_Swapin3", "Body_Swapin4", "Body_Swapin5", "Body_Swapout1",        #31
    "Body_Swapout2", "Body_Swapout3", "Body_Swapout4", "Body_Swapout5"     #35
    ]
    
intense = []

logger = None
HAPTIC_DELAY = 25
def init_haptic() :
    global logger
    if IS_HAPTIC :
        player.initialize()
        for n in tacts :
            player.register("a"+n, "./PUBG/TactFiles/a"+n+".tact")
        # for n in tacts :
        #     player.register("b"+n, "./PUBG/TactFiles/b"+n+".tact")
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)
    logger.setLevel(level= logging.DEBUG)
    # logging.basicConfig(level = logging.DEBUG)

    f = open("./PUBG/TactFiles/intense.txt", 'r')
    for i in range(len(tacts)):
        hapval = 1
        try:
            hapval = float(f.readline())
        except ValueError :
            hapval = 1
        intense.append(hapval)
    f.close()

haptype = "a"
def abtest() :
    global haptype
    if haptype == "a" :
        haptype = "b"
    else :
        haptype = "a"
    print("haptype changed : ", haptype)

haptic_type = -1   #haptic type
haptic_intensity = 1.0
def active(hapnum, overlap = False, alt = "alt", dur = 1) :
    global haptic_type
    # print("active", haptic_type, hapnum, player.is_playing())
    if haptic_type != hapnum  and hapnum != -1 and haptic_type != 9 and not player.is_playing_key(alt):
        haptic_type = hapnum
        msg = "hatpic : " + haptype + tacts[hapnum]
        GUI.hap_change(tacts[hapnum])
        logger.info(msg)
        # print("hatpic : ", haptype + tacts[hapnum])
        if IS_HAPTIC :
            player.submit_registered_with_option(haptype + tacts[hapnum], alt,
                                     scale_option={"intensity": intense[hapnum], "duration": dur},
                                     rotation_option={"offsetAngleX": 0, "offsetY": 0})
    elif haptic_type == hapnum or haptic_type == 9:
        # print(player.is_playing())
        if (not player.is_playing() or overlap) and IS_HAPTIC :
            haptic_type = hapnum
            msg = "ahatpic : " + haptype + tacts[hapnum]
            GUI.hap_change(tacts[hapnum])
            logger.info(msg)
            # print("hatpic : ", haptype + tacts[hapnum])
            player.submit_registered_with_option(haptype + tacts[hapnum], alt,
                                     scale_option={"intensity": intense[hapnum], "duration": dur},
                                     rotation_option={"offsetAngleX": 0, "offsetY": 0})

def GUI_active(hap_name) :
    for i in range(len(tacts)) :
        if tacts[i] == hap_name :
            msg = "hatpic : " + haptype + hap_name
            logger.info(msg)
            player.submit_registered_with_option(haptype + hap_name, "alt",
                                     scale_option={"intensity": intense[i], "duration": 1},
                                     rotation_option={"offsetAngleX": 0, "offsetY": 0})

def intensity_up() :
    global haptic_intensity
    if haptic_intensity <10 :
        haptic_intensity += 0.1
        print("intensity_up", haptic_intensity)
        active(24)      #Body_Hapup

def intensity_down() :
    global haptic_intensity
    if haptic_intensity >= 0 :
        haptic_intensity -= 0.1
        print("intensity_down", haptic_intensity)
        active(25)     #Body_Hapdown

def ingame(arr) :
    global haptic_type
    if(arr[1]) :
        active(9, alt = "a1")   #Body_Kill
    if(arr[6]) :
        active(2, alt = "a6")   #Body_Bluezone
    if(arr[0]) :
        active(4, True, alt = "a0")   #Body_Damage
    if(arr[2]) :
        active(6, True, alt = "a2")  #Body_Fire
    if(arr[5]) :
        active(0, alt = "a5")  #Body_Action
    if(arr[7]) :
        active(5, alt= "a7", dur = 1-arr[7]/150)
        # if (0<arr[7]<10) :
        #     active(5, alt = "a7")
        # elif(10<=arr[7]<40) :
        #     active(17, alt = "a7")
        # elif(arr[7]>=40) :
        #     active(3, alt = "a7")  #Body_Car
    if(arr[8]) :
        active(14, True , alt = "a8")  #Body_Reload
    if(arr[9]) :
        temp = arr[9]
        if temp == 100 :
            active(13, True, alt = "a9")   #Body_Swapwheel
        else :
            swap(temp)
    # elif(arr[3]) :
    #     active(5,2)  #Body_Run
    if(arr[11]) :
        active(16, alt = "a11")  #Body_Heartbeat


punch_stack = -1
def punch() :
    global punch_stack
    if punch_stack == 1 :
        active(19, alt = "punch1")
    else :
        active(19,  alt = "punch2")
    punch_stack *= -1


def swap(num) :
    a = num//10
    b = num%10
    if a != 0 :
        active(25+a, alt = "a9")
        sleep(0.2)
    if b != 0 :
        active(30+b, alt = "a9")

def throw() :
    active(8)

def fire() :
    active(6, True)

def pose(n) :
    if n == 0 :
        active(20)
    elif n == 1 :
        active(21)
    elif n == 2:
        active(22)

def interact() :
    active(23)

def aim() :
    active(15)  #Body_Aim

def swapin(n) :
    if n == 3 :
        active(26)  #Body_Swapin2
    elif n == 4 :
        active(25)  #Body_Swapin1

def airplane() :
    active(1)       #Body_Airplane

def landing() :
    active(12)
def fall(n) :
    if n==1 :
        active(7)
    elif n==2 :
        active(11, alt = "alt2")
    elif n==3 :
        active(10)

# init_haptic()
# while(True) :
#     player.submit_registered_with_option("aBody_Airplane", "alt",
#                             scale_option={"intensity": haptic_intensity, "duration": 1},
#                             rotation_option={"offsetAngleX": 0, "offsetY": 0})

    # print('is_playing', player.is_playing())