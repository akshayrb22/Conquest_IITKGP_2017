import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import PIL
from PIL import Image
import math
import matplotlib.pyplot as plot
import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []
    
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id):
        return id not in self.obstacles
    
    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results
class SimpleGraph:
    def __init__(self):
        self.edges = {}
    
    def neighbors(self, id):
        return self.edges[id]
graph=Grid(600,570)


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
    img = Image.open('as.jpg')
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    img.save('asia.jpg')
    image = cv2.imread('asia.jpg',1)

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

    lower_bl = np.array([100,43,145])
    upper_bl = np.array([113,161,194])
        
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
                if(area2>17):
                    if(shape2=='circle' or shape2=='square' or shape2=='rectangle' or shape2=='triangle'):
                        if(area2>255):   
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
                            cv2.putText(resized, shape3+'y', (cX2, cY2), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
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
    print(aa)

    resized[np.where((resized == [255,cc[0],0]).all(axis = 2))] = [0,0,255]
    resized[np.where((resized == [255,cc[17],0]).all(axis = 2))] = [0,255,255]
    
    gray3 = cv2.cvtColor(resbl, cv2.COLOR_BGR2GRAY)
    blurred3 = cv2.GaussianBlur(gray3, (5, 5), 0)
    thresh3 = cv2.threshold(blurred3, t2, 255, cv2.THRESH_BINARY)[1]
    edges3 = cv2.Canny(thresh3,e12,e12)
    edgess3= imutils.resize(edges3, width=600)
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
                area3=cv2.contourArea(c3)
                rat13=area/6.25 + 900
                rat23=area/6.25 + 200
                if(area3>rat23 and area3<rat13):
                    shape4='sqr'
                elif(area3>(rat23/2) and area3<(rat13/2)+400):
                    shape4='trng'
                else:
                    shape4='null'
                if(area3>17):
                    if(shap=='circle' or shap=='square' or shap=='rectangle' or shap=='triangle'):
                        cv2.drawContours(resized, [c3], -1, (0, 255, 0), 2)
                        cv2.circle(resized, (cX3, cY3), 3, (255, 0, 0), -1)

                        #print(area3)
                        cv2.putText(resized, shape4+'b', (cX3, cY3), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)

    
    img = cv2.imread('asia.jpg')
    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        distance=float((((x1-x2)*(x1-x2))+((y1-y2)*(y1-y2)))^(1/2))
        return distance
    u=0
    v=0
    for i in range(0,600):
        for j in range(0,570):
            cv2.line(img,(u,0),(u,570),(255,0,0),1)
            cv2.line(img,(0,v),(600,v),(255,0,0),1)
            u+=30
            v+=30


            frontier = PriorityQueue()
            frontier.put((cX,cY), 0)
            came_from = {}
            cost_so_far = {}
            came_from[(cX,cY)] = None
            cost_so_far[(cX,cY)] = 0
            for n in range(0,19):
                for n in range(0,19):
                    while not frontier.empty():
                        current = frontier.get()
                        if current == (cX2,cY2):
                            break
                        for next in graph.neighbors(current):
                            new_cost = cost_so_far[current] + 1
                            if next not in cost_so_far or new_cost < cost_so_far[next]:
                                cost_so_far[next] = new_cost
                                priority = new_cost + heuristic((cX2,cY2), next)
                                frontier.put(next, priority)
                                came_from[next] = current
                                

                                


    cv2.imshow('asia',img)

    #cv2.imshow('frame',resized)
    cv2.imshow('mask',resized)
    #cv2.imshow('fme',resbl)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
#cap.release()
cv2.destroyAllWindows()
