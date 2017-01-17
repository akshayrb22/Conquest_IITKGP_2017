import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import PIL
from PIL import Image

while(True):
    image = cv2.imread('p.png',1)
    resized = imutils.resize(image, width=600)
    ratio = image.shape[0] / float(resized.shape[0])
    


    
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    
    lower_y = np.array([0,0,96])
    upper_y = np.array([79,255,255])
        
    masky = cv2.inRange(hsv, lower_y, upper_y)
        
    lower_b = np.array([164,0,96])
    upper_b = np.array([255,255,255])
        
    maskb = cv2.inRange(hsv, lower_b, upper_b)

    resy = cv2.bitwise_and(resized,resized, mask= masky)
    resb = cv2.bitwise_and(resized,resized, mask= maskb)
    
    grayy = cv2.cvtColor(resy, cv2.COLOR_BGR2GRAY)
    grayb = cv2.cvtColor(resb, cv2.COLOR_BGR2GRAY)

    threshy = cv2.threshold(grayy, 120, 255, cv2.THRESH_BINARY)[1]
    edgesy = cv2.Canny(threshy,100,100)

    threshb = cv2.threshold(grayb, 120, 255, cv2.THRESH_BINARY)[1]
    edgesb = cv2.Canny(threshb,100,100)

    cnts = cv2.findContours(edgesb.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # loop over the contours
    for c in cnts:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            

            if M["m00"] > 0:
                cX = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
                cY = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                area=cv2.contourArea(c)
                cv2.drawContours(resb, [c], -1, (0, 255, 0), 2)
                cv2.putText(resb, ' town hall', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 1)
                
    cv2.imshow('maskb',resb)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

