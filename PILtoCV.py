import numpy
import cv2 as cv
import numpy as np

def PILtoCV(pil_image) :
    open_cv_image = numpy.array(pil_image) 
    open_cv_image = open_cv_image[:, :, ::-1]
    return open_cv_image 
