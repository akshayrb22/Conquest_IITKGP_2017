import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import PIL
from PIL import Image
import math
import utils
from Frame import Frame
from gray_blur import GrayBlurThresh

obj = Frame()
obj.cap_frame()
image,resized,ratio=obj.find_ratio()


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

lower_gre = np.array([48,77,28])          #green
upper_gre = np.array([87,255,132])
    
maskg = cv2.inRange(hsv, lower_gre, upper_gre)

lower_red = np.array([155,106,133])          #red
upper_red = np.array([208,177,186])
    
maskr = cv2.inRange(hsv, lower_red, upper_red)

res = cv2.bitwise_and(resized,resized, mask= masky)
resb = cv2.bitwise_and(resized,resized, mask= maskb)
resbl = cv2.bitwise_and(resized,resized, mask= maskbl)
resg = cv2.bitwise_and(resized,resized, mask= maskg)
resr = cv2.bitwise_and(resized,resized, mask= maskr)


yellow=GrayBlurThresh(res)
Brown=GrayBlurThresh(resb)
Blue=GrayBlurThresh(resbl)
Green=GrayBlurThresh(resg)
Red=GrayBlurThresh(resr)




##town hall part
red_cnt=Red.GBT_AREA()
green_cnt=Green.GBT_AREA()
redX,redY=Red.get_center(red_cnt)
greenX,greenY=Green.get_center(green_cnt)
bX=(redX+greenX)/2
bY=(redY+greenY)/2


if(bcontours>20):#this is to draw the contours for the town hall
    cv2.drawContours(resized, red_cnt, -1, (0, 255, 0), 2)
    cv2.drawContours(resized, green_cnt, -1, (0, 255, 0), 2)
    cv2.putText(resized, ' town hall', red_cnt, cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
    cv2.circle(resized, (bX,bY),3 , (0, 0, 0), -1)
   
#resources
c=0
cyan=255
k=0
noe=18

dd=np.zeros(shape=(noe))
cc=np.zeros(shape=(noe))
aa=np.zeros(shape=(noe))


while c<30:  
    ycontours[c]=Yellow.GBT_AREA()
    yellow_x[c],yellow_y[c]=Yellow.get_center()
    

    rat1=ycontours[c]/6.25 + 800
    rat2=ycontours[c]/6.25 + 200
    dd[c]=distance(bX,bY,yellow_x,yellow_y)
    if ycontours[c] in range(rate1,rate2):
        shape3='sqr'
    elif ycontours[c] in range((rate1/2),(rate2/2)):
        shape3='trng'
    else:
        shape3='null'
    if (area2>255):
        m_ang[c]=angle_for_marker()
    
    c=c+1






for n in range(0,18):#code for arranging arrays according to length
        for l in range(0,17):
            if dd[l]>dd[1+l]:
                p=dd[l]
                dd[l]=dd[l+1]
                dd[l+1]=p
                      

                s=ycontours[l]
                ycontours[l]=ycontours[l+1]
                ycontours[l+1]=s

                r_angle=aa[l]
                aa[l]=aa[l+1]
                aa[l+1]=r_angle

                y_center=yellow_center[l]
                yellow_center[l]=yellow_center[l+1]
                yellow_center[l+1]=y_center

                

                
    
host = "192.168.43.1:8080"
if len(sys.argv)>1:
    host = sys.argv[1]

hoststr = 'http://' + host + '/video'
print 'Streaming ' + hoststr

stream=urllib2.urlopen(hoststr)
flag=1
bytes=''    



while(True):

    vid_cap()
    
    
    
    
