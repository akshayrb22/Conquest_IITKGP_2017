import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils

def nothing(x):
    pass
cv2.namedWindow('image')

cv2.createTrackbar('H','image',0,255,nothing)
cv2.createTrackbar('S','image',0,255,nothing)
cv2.createTrackbar('V','image',0,255,nothing)
cv2.createTrackbar('h','image',0,255,nothing)
cv2.createTrackbar('s','image',0,255,nothing)
cv2.createTrackbar('v','image',0,255,nothing)
cv2.createTrackbar('t','image',0,255,nothing)


while(1):
        image = cv2.imread('11.jpg',1)
        resized = imutils.resize(image, width=600)
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)


        H = cv2.getTrackbarPos('H','image')
        S = cv2.getTrackbarPos('S','image')
        V = cv2.getTrackbarPos('V','image')
        
        h = cv2.getTrackbarPos('h','image')
        s = cv2.getTrackbarPos('s','image')
        v = cv2.getTrackbarPos('v','image')
        t = cv2.getTrackbarPos('t','image')



    
        lower_blue = np.array([h,s,v])
        upper_blue = np.array([H,S,V])
        
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        res = cv2.bitwise_and(resized,resized, mask= mask)
        gray3 = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred3 = cv2.GaussianBlur(gray3, (5, 5), 0)
        thresh3 = cv2.threshold(blurred3, t, 255, cv2.THRESH_BINARY)[1]
        edges3 = cv2.Canny(thresh3,0,0)

        cv2.imshow('frame',edges3)
        cv2.imshow('mask',mask)
        cv2.imshow('res',res)
        k = cv2.waitKey(5) & 0xFF
        if k == 32:
            break

cv2.destroyAllWindows()        
