import cv2
import numpy as np
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
            res,frame =  cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


            H = cv2.getTrackbarPos('H','image')
            S = cv2.getTrackbarPos('S','image')
            V = cv2.getTrackbarPos('V','image')
            
            h = cv2.getTrackbarPos('h','image')
            s = cv2.getTrackbarPos('s','image')
            v = cv2.getTrackbarPos('v','image')



        
            lower_blue = np.array([h,s,v])
            upper_blue = np.array([H,S,V])
            
            mask = cv2.inRange(hsv, lower_blue, upper_blue)

            res = cv2.bitwise_and(frame,frame, mask= mask)

            cv2.imshow('frame',frame)
            cv2.imshow('mask',mask)
            cv2.imshow('res',res)
            k = cv2.waitKey(5) & 0xFF
            if k == 32:
                break

cv2.destroyAllWindows()        

