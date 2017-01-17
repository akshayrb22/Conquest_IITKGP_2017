import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils

cap = cv2.VideoCapture(0)

def nothing(x):
    pass
cv2.namedWindow('frame')
cv2.createTrackbar('h','frame',0,255,nothing)
cv2.createTrackbar('s','frame',0,255,nothing)
cv2.createTrackbar('v','frame',0,255,nothing)
cv2.createTrackbar('H','frame',0,255,nothing)
cv2.createTrackbar('S','frame',0,255,nothing)
cv2.createTrackbar('V','frame',0,255,nothing)

while(True):
    # Capture frame-by-frame
    ret, image = cap.read()

    # Our operations on the frame come here
    

    resized = imutils.resize(image, width=600)
    ratio = image.shape[0] / float(resized.shape[0])


    # convert the resized image to grayscale, blur it slightly,
    # and threshold it

    h = cv2.getTrackbarPos('h','frame')
    s = cv2.getTrackbarPos('s','frame')
    v = cv2.getTrackbarPos('v','frame')
    H = cv2.getTrackbarPos('H','frame')
    S = cv2.getTrackbarPos('S','frame')
    V = cv2.getTrackbarPos('V','frame')
    
    
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    
    lower_y = np.array([h,s,v])
    upper_y = np.array([H,S,V])
        
    masky = cv2.inRange(hsv, lower_y, upper_y)

    res = cv2.bitwise_and(resized,resized, mask= masky)
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)[1]
    edges = cv2.Canny(thresh,0,0)
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    sd = ShapeDetector()

    # loop over the contours
    for c in cnts:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            

            if M["m00"] > 0:
                cX = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
                cY = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
                shape = sd.detect(c)
                if (shape=="circle")==False:
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                    c = c.astype("float")
                    c *= ratio
                    c = c.astype("int")
                    area=cv2.contourArea(c)
                    if(area>0):
                        cv2.drawContours(resized, [c], -1, (0, 255, 0), 2)
                        cv2.putText(resized, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)

    cv2.imshow('frame',resized)
    cv2.imshow('mask',res)
    cv2.imshow('frae',edges)
    cv2.imshow('fme',thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
