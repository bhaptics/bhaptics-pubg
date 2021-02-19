import imgconvert as conv
from PILtoCV import PILtoCV
import cv2 as cv
import d3dshot

d = None
def init_screenshot() :
    global d
    d = d3dshot.create(capture_output="numpy")

    tempimg = d.screenshot()
    conv.init_convert(tempimg)

def screenshottaker() :
    global d
    return conv.imgconvert(d.screenshot())

# init_screenshot()