##Assign to Akshay
##Functionalities required-
##  capture frame(single image for resource & obsatcle processing)
##  capture video
##  find bot
##  find resources,obstacles,town hall
##  resizing, ratio


import numpy as np
import cv2
import PIL
from PIL import Image
import imutils
from Point import Point
from HSV import Color

class Frame(object):
    elements = []
    camera = None
    image = None
    res = None
    ratio = None
    resized = None
    @staticmethod
    def connect( cameraID):
        Frame.camera = cv2.VideoCapture(cameraID)
        

    @staticmethod
    def cap_frame():
        Frame.res, Frame.image = Frame.camera.read()
    @staticmethod
    def find_ratio():
        Frame.resized = imutils.resize(Frame.image, height=600)
        Frame.ratio = Frame.image.shape[0] / float(Frame.resized.shape[0])
        return Frame.image, Frame.resized, Frame.ratio
    @staticmethod
    def get_center_color(color):
        lower_color = Color.Color(color, 0)
        upper_color = Color.Color(color, 1)
        hsv = cv2.cvtColor(Frame.resized, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color.get_array(), upper_color.get_array())

    @staticmethod
    def get_center_from_contour(contour):
        for c in contour:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            Moment = cv2.moments(c)
            

            if Moment["m00"] > 0:
                point = Point()
                point.x = int((Moment["m10"] / Moment["m00"]+ 1e-7) * Frame.ratio)#uses moment of inertia concept
                point.y = int((Moment["m01"] / Moment["m00"]+ 1e-7) * Frame.ratio)
                shape = sd.detect(c)
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c = c.astype("float")
                c *= Frame.ratio
                c = c.astype("int")
                area=cv2.contourArea(c)
                print point.toString()
                return point        


if __name__ == '__main__':
    Frame.connect(0)
    while True:
        Frame.cap_frame()
        Frame.find_ratio()
        cv2.imwrite("frame.jpg", Frame.image)
        cv2.imshow("frame.jpg", Frame.image)
        #rame.get_center_color("red")
    quit()