import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import urllib2
import sys
from Color import Color

colorName =raw_input("Enter the color : ")
upperColor = Color(colorName,1)
lowerColor = Color(colorName,0)
cap=cv2.VideoCapture(0)

def HSVProcess(x):

    upperColor.H = cv2.getTrackbarPos('H','img')
    upperColor.S = cv2.getTrackbarPos('S','img')
    upperColor.V = cv2.getTrackbarPos('V','img')
    
    lowerColor.H = cv2.getTrackbarPos('h','img')
    lowerColor.S = cv2.getTrackbarPos('s','img')
    lowerColor.V = cv2.getTrackbarPos('v','img')
    lowerColor.T = cv2.getTrackbarPos('t','img')
    #t = cv2.getTrackbarPos('t','img')
    p=open(  colorName + ".txt","w")
    p.write(upperColor.toString() + "," + lowerColor.toString() + "," + str(lowerColor.T))
cv2.namedWindow('img',cv2.WINDOW_NORMAL)

cv2.createTrackbar('H','img',int(upperColor.H),255,HSVProcess)
cv2.createTrackbar('S','img',int(upperColor.S),255,HSVProcess)
cv2.createTrackbar('V','img',int(upperColor.V),255,HSVProcess)
cv2.createTrackbar('h','img',int(lowerColor.H),255,HSVProcess)
cv2.createTrackbar('s','img',int(lowerColor.S),255,HSVProcess)
cv2.createTrackbar('v','img',int(lowerColor.V),255,HSVProcess)
cv2.createTrackbar('t','img',int(lowerColor.T),255,HSVProcess)
cv2.createTrackbar('e1','img',0,255,HSVProcess)


while(1):
 
        res, i = cap.read(1)
        resized = imutils.resize(i, width=690)
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

        #t = cv2.getTrackbarPos('t','img')

        mask = cv2.inRange(hsv, lowerColor.get_array(), upperColor.get_array())

        res = cv2.bitwise_and(resized,resized, mask= mask)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        b = cv2.threshold(blurred, float(lowerColor.T), 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.threshold(b, 0, 255, cv2.THRESH_BINARY)[1]
        edges = cv2.Canny(b,0,0)
        
        cv2.imshow('frame',edges)
        cv2.imshow('mask',mask)
        cv2.imshow('resized',res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

cv2.destroyAllWindows() 
