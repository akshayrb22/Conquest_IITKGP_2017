import numpy as np
import cv2
import PIL
from PIL import Image
import imutils
from pyimagesearch.shapedetector import ShapeDetector
from Frame import Frame
a=Frame()

class GrayBlurThresh:
    global area 
    global center_point
    global cX
    global cY
    
    def __init__(self,Image):
        self.image=Image
        area=0
        center_point=(0,0)
            


    def GBT_AREA(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        t = cv2.getTrackbarPos('t','frame')
        e1 = cv2.getTrackbarPos('e1','frame')
        e2 = cv2.getTrackbarPos('e2','frame')

        thresh = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)[1]
        edges = cv2.Canny(thresh,e1,e1)
        edgess = imutils.resize(edges, width=600)
        # find contours in the thresholded image and initialize the
        # shape detector
        cnts = cv2.findContours(edgess.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        sd = ShapeDetector()
        return cnts        

    def get_center(self,contour):
        for c in contour:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            

            if M["m00"] > 0:
                cX = int((M["m10"] / M["m00"]+ 1e-7) * ratio)#uses moment of inertia concept
                cY = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
                shape = sd.detect(c)
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                area=cv2.contourArea(c)
                print cX,cY
                center_point=(cX,cY)
                return cX,cY
img=cv2.imread('asia.jpg',1)
obj=GrayBlurThresh(img)
cont=obj.GBT_AREA()
obj.get_center(cont)






    
            
