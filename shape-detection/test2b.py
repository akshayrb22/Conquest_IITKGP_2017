import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
cap=cv2.VideoCapture(0)

def nothing(x):
    pass
cv2.namedWindow('image')

cv2.createTrackbar('H','image',0,255,nothing)
cv2.createTrackbar('S','image',0,255,nothing)
cv2.createTrackbar('V','image',0,255,nothing)
cv2.createTrackbar('h','image',0,255,nothing)
cv2.createTrackbar('s','image',0,255,nothing)
cv2.createTrackbar('v','image',0,255,nothing)

while(1):
    res,frame=cap.read()
    image = cv2.imread('llooll.jpg',1)
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    H=cv2.getTrackbarPos('H','image')
    S=cv2.getTrackbarPos('S','image')
    V=cv2.getTrackbarPos('V','image')
    h=cv2.getTrackbarPos('h','image')
    s=cv2.getTrackbarPos('s','image')
    v=cv2.getTrackbarPos('v','image')


    lower_blue=np.array([h,s,v])
    upper_blue=np.array([H,S,V])
    mask=cv2.inRange(hsv,lower_blue,upper_blue)
    res=cv2.bitwise_and(image,image,mask=mask)
    cv2.imshow('frame',image)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()                     
