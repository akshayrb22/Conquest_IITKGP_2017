import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import PIL
from PIL import Image
import math


#cap = cv2.VideoCapture(0)

def nothing(x):
    pass

def swap(A,x,y):
    tmp = A[x]
    A[x]=A[y]
    A[y]=tmp
                


cv2.namedWindow('frame')
cv2.createTrackbar('t','frame',0,255,nothing)
cv2.createTrackbar('e1','frame',0,255,nothing)
cv2.createTrackbar('e2','frame',0,1500,nothing)
cv2.namedWindow('frameb')
cv2.createTrackbar('t2','frameb',0,255,nothing)
cv2.createTrackbar('e12','frameb',0,255,nothing)
cv2.createTrackbar('e22','frameb',0,255,nothing)

while(True):
    # Capture frame-by-frame
    #ret, image = cap.read()
    baseheight = 570
    img = Image.open('1.jpg')
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    img.save('11.jpg')
    image = cv2.imread('11.jpg',1)

    # Our operations on the frame come here
 
    resized = imutils.resize(image, width=620)
    ratio = image.shape[0] / float(resized.shape[0])


    # convert the resized image to grayscale, blur it slightly,
    # and threshold it

    
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    
    lower_y = np.array([22,9,0])
    upper_y = np.array([80,255,219])
        
    masky = cv2.inRange(hsv, lower_y, upper_y)

        
    lower_b = np.array([4,0,0])
    upper_b = np.array([22,255,255])
        
    maskb = cv2.inRange(hsv, lower_b, upper_b)

    lower_bl = np.array([81,135,94])
    upper_bl = np.array([101,255,255])
        
    maskbl = cv2.inRange(hsv, lower_bl, upper_bl)

    res = cv2.bitwise_and(resized,resized, mask= masky)
    resb = cv2.bitwise_and(resized,resized, mask= maskb)
    resbl = cv2.bitwise_and(resized,resized, mask= maskbl)



    
    gray = cv2.cvtColor(resb, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    t = cv2.getTrackbarPos('t','frame')
    e1 = cv2.getTrackbarPos('e1','frame')
    e2 = cv2.getTrackbarPos('e2','frame')
    
    thresh = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY)[1]
    edges = cv2.Canny(thresh,e1,e1)
    edgess = imutils.resize(edges, width=600)
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    sd = ShapeDetector()
    area=0
    cX=0
    cY=0
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
                if(area>0):
                    cv2.drawContours(resized, [c], -1, (0, 255, 0), 2)
                    cv2.putText(resized, ' town hall', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
                    cv2.circle(resized, (cX, cY),3 , (0, 0, 0), -1)

              



    gray2 = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    blurred2 = cv2.GaussianBlur(gray2, (5, 5), 0)
    t2 = cv2.getTrackbarPos('t2','frameb')
    e12 = cv2.getTrackbarPos('e12','frameb')
    e22 = cv2.getTrackbarPos('e22','frameb')
    thresh2 = cv2.threshold(blurred2, 50, 255, cv2.THRESH_BINARY)[1]
    edges2 = cv2.Canny(thresh2,e12,e12)
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts2 = cv2.findContours(edges2.copy(), cv2.RETR_EXTERNAL,
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
    for c2 in cnts2:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c2)
            

            if M["m00"] > 0:
                cX2 = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
                cY2 = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
                shape2 = sd.detect(c2)
                
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c2 = c2.astype("float")
                c2 *= ratio
                c2 = c2.astype("int")
                area2=cv2.contourArea(c2)
                rat1=area/6.25 + 800
                rat2=area/6.25 + 200
                if(area2>rat2 and area2<rat1):
                    shape3='sqr'
                elif(area2>(rat2/2) and area2<(rat1/2)+400):
                    shape3='trng'
                else:
                    shape3='null'
                if(area2>0):
                    if(shape2=='circle' or shape2=='square' or shape2=='rectangle' or shape2=='triangle'):
                        if(area2>0):   
                            dist2=float((((cX-cX)*(cX-cX))+((cY-cY2)*(cY-cY2)))^(1/2))
                            dist=float((((cX-cX2)*(cX-cX2))+((cY-cY2)*(cY-cY2)))^(1/2))
                            sinn=float(dist2/dist)
                            angle = math.acos(float(sinn))
                            j=round(math.degrees(angle),2)
                            if cX2>cX and cY2>cY:
                                quad=4
                                j=270+j
                            elif cX2<cX and cY2>cY:
                                quad=3
                                j=270-j
                            elif cX2<cX and cY2<cY:
                                quad=2
                                j=j+90
                            else:
                                quad=1
                                j=90-j
                            
                            xx[k]=cX2
                            yy[k]=cY2
                            dd[k]=dist
                            cc[k]=cyan
                            aa[k]=j
                            qq[k]=quad
                            
                            k=k+1
                            cv2.drawContours(resized, [c2], -1, (0, 255, 0), 2)
                            cv2.circle(resized, (cX2, cY2), 3, (0,0,255), -1)
                            cv2.putText(resized,'y', (cX2, cY2), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
                            cv2.line(resized,(cX,cY),(cX2,cY2),(255,cyan,0),2)
                            cyan=cyan-1



    

    for n in range(0,18):
        for l in range(0,17):
            if dd[l]>dd[1+l]:
                p=dd[l]
                dd[l]=dd[l+1]
                dd[l+1]=p
                
                q=xx[l]
                xx[l]=xx[l+1]
                xx[l+1]=q
                
                r=yy[l]
                yy[l]=yy[l+1]
                yy[l+1]=r

                s=cc[l]
                cc[l]=cc[l+1]
                cc[l+1]=s

                t=aa[l]
                aa[l]=aa[l+1]
                aa[l+1]=t

                u=qq[l]
                qq[l]=qq[l+1]
                qq[l+1]=u
                
                        
    #print(xx,yy)
    #print(dd)
    #print(cc)
    #print(aa)

    resized[np.where((resized == [255,cc[0],0]).all(axis = 2))] = [0,0,255]
    resized[np.where((resized == [255,cc[17],0]).all(axis = 2))] = [0,255,255]
    
    gray3 = cv2.cvtColor(resbl, cv2.COLOR_BGR2GRAY)
    blurred3 = cv2.GaussianBlur(gray3, (5, 5), 0)
    thresh3 = cv2.threshold(blurred3, 50, 255, cv2.THRESH_BINARY)[1]
    edges3 = cv2.Canny(thresh3,e12,e12)
    # find contours in the thresholded image and initialize the
    # shape detector
    cnts3 = cv2.findContours(edges3.copy(), cv2.RETR_EXTERNAL,
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
                area3=cv2.contourArea(c3)
                rat13=area/6.25 + 900
                rat23=area/6.25 + 200
                if(area3>rat23 and area3<rat13):
                    shape4='sqr'
                elif(area3>(rat23/2) and area3<(rat13/2)+400):
                    shape4='trng'
                else:
                    shape4='null'
                if(area3>0):
                    if(shap=='circle' or shap=='square' or shap=='rectangle' or shap=='triangle'):
                        cv2.drawContours(resized, [c3], -1, (0, 255, 0), 2)
                        cv2.circle(resized, (cX3, cY3), 3, (255, 0, 0), -1)

                        #print(area3)
                        cv2.putText(resized, 'b', (cX3, cY3), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)



    cv2.imshow('fre',resized)
    #cv2.imshow('mask',resb)
    #cv2.imshow('fme',resbl)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
#cap.release()
cv2.destroyAllWindows()

