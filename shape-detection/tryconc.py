import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import PIL
from PIL import Image
import math

def nothing(x):
    pass

while(True):
    # Capture frame-by-frame
    #ret, image = cap.read()
    baseheight = 570
    img = Image.open('1.jpg')
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    img.save('sych.jpg')
    image = cv2.imread('sych.jpg',1)
    cv2.namedWindow('frameb')
    cv2.createTrackbar('t2','frameb',0,255,nothing)
    cv2.createTrackbar('e12','frameb',0,255,nothing)
    cv2.createTrackbar('e22','frameb',0,255,nothing)

    # Our operations on the frame come here
 
    resized = imutils.resize(image, width=600)
    ratio = image.shape[0] / float(resized.shape[0])


    # convert the resized image to grayscale, blur it slightly,
    # and threshold it

    
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    
    lower_y = np.array([0,0,178])
    upper_y = np.array([255,92,255])
        
    masky = cv2.inRange(hsv, lower_y, upper_y)
        
    lower_b = np.array([10,79,132])
    upper_b = np.array([19,170,255])
        
    maskb = cv2.inRange(hsv, lower_b, upper_b)

    lower_bl = np.array([75,125,103])
    upper_bl = np.array([120,255,255])
        
    maskbl = cv2.inRange(hsv, lower_bl, upper_bl)

    res = cv2.bitwise_and(resized,resized, mask= masky)
    resb = cv2.bitwise_and(resized,resized, mask= maskb)
    resbl = cv2.bitwise_and(resized,resized, mask= maskbl)



    
    gray = cv2.cvtColor(resb, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    t = cv2.getTrackbarPos('t','frame')
    e1 = cv2.getTrackbarPos('e1','frame')
    e2 = cv2.getTrackbarPos('e2','frame')
    
    thresh = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY)[1]
    edges = cv2.Canny(thresh,e1,e1)
    edgess = imutils.resize(edges, width=600)
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(edgess.copy(), cv2.RETR_EXTERNAL,
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
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                area=cv2.contourArea(c)
                if(area>20):
                    cv2.drawContours(resized, [c], -1, (0, 255, 0), 2)
                    cv2.putText(resized, ' town hall', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
                    cv2.circle(resized, (cX, cY),3 , (0, 0, 0), -1)
              



    gray2 = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    blurred2 = cv2.GaussianBlur(gray2, (5, 5), 0)
    t2 = cv2.getTrackbarPos('t2','frameb')
    e12 = cv2.getTrackbarPos('e12','frameb')
    e22 = cv2.getTrackbarPos('e22','frameb')
    thresh2 = cv2.threshold(blurred2, t2, 255, cv2.THRESH_BINARY)[1]
    edges2 = cv2.Canny(thresh2,e12,e12)
    edgess2= imutils.resize(edges2, width=600)
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts2 = cv2.findContours(edgess2.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = cnts[0] if imutils.is_cv2() else cnts2[1]
    sd2 = ShapeDetector()
    cyan=255
    k=0
    noe=18
    xx=np.zeros(shape=(noe))
    yy=np.zeros(shape=(noe))
    dd=np.zeros(shape=(noe))
    cc=np.zeros(shape=(noe))
    aa=np.zeros(shape=(noe))
    qq=np.zeros(shape=(noe))
    # loop over the contours
    gray3 = cv2.cvtColor(resbl, cv2.COLOR_BGR2GRAY)
    blurred3 = cv2.GaussianBlur(gray3, (5, 5), 0)
    thresh3 = cv2.threshold(gray3, t2, 255, cv2.THRESH_BINARY)[1]
    edges3 = cv2.Canny(thresh3,e12,e12)
    edgess3= imutils.resize(edges3, width=578)
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts3 = cv2.findContours(edgess3.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cnts3 = cnts3[0] if imutils.is_cv2() else cnts3[1]
    sd3 = ShapeDetector()

    # loop over the contours
    for c3 in cnts3:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c3)
            

            if M["m00"] > 0:
                cX3 = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
                cY3 = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
                shap = sd3.detect(c3)
                
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c3 = c3.astype("float")
                c3 *= ratio
                c3 = c3.astype("int")
                cv2.drawContours(resized, [c3], -1, (255, 0, 255), 2)
                cv2.circle(resized, (cX3, cY3), 1, (255, 0, ), -1)
                cv2.rectangle(resized,(cX3-15,cY3-15),(cX3+15,cY3+15),(0,255,0),1)

                #print(area3)
    cv2.imshow('mask',resized)
    
    #cv2.imshow('fme',resbl)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
#cap.release()
cv2.destroyAllWindows()
