import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import PIL
from PIL import Image
import math              
import bluetooth
import urllib2
import sys
import turn_2

target_name = "raspberrypi"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print "found target bluetooth device with address ", target_address
else:
    print "could not find target bluetooth device nearby"

bd_addr = "B8:27:EB:26:F6:A4"

port = 1

##sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
##host = "192.168.43.1:8080"
##if len(sys.argv)>1:
##    host = sys.argv[1]
##
##hoststr = 'http://' + host + '/video'
##print 'Streaming ' + hoststr
##
##stream=urllib2.urlopen(hoststr)
##flagip=0
##k=0
##bytes=''
noe=18
xx=np.zeros(shape=(noe))
yy=np.zeros(shape=(noe))
dd=np.zeros(shape=(noe))
cc=np.zeros(shape=(noe))
aa=np.zeros(shape=(noe))
qq=np.zeros(shape=(noe))
ff=np.zeros(shape=(noe))

def bluetoothConnect():
    sock.connect((bd_addr, port))

def bluetoothDisconnect():
    sock.close()

def return_to_twn():
    print('l')
    
#cap = cv2.VideoCapture(0)
def trackerOnRes(a,botcx,botcy):
    k=50
    if((botcx>xx[a]-k and botcx<xx[a]+k)and(botcy>yy[a]-k and botcy<yy[a]+k)) :
        return 1
    else:
        return 0
    
def MainExecute():
    x,y,z=trackerAngle()
    print(x,y,z)
    for n in range(0,18):
        gotores(n,x,y,z)
        return_to_twn()
        
    
    

def gotores(a,current_angle,botcx,botcy):
    angle_res=aa[a]
    if(trackerOnRes(a,botcx,botcy)==True):
        socket.send("s")
        socket.send("b")
        ff[a]=ff[a]-1
        if ff[a]==0:
            numpy.delete(ff,a,axis=1)
        gotores(a,current_angle,botcx,botcy)
    else:        
        trackerAngle()
        go_to_direction(current_angle,aa)
               
        
    
def nothing(x):
    pass

def swap(A,x,y):
    tmp = A[x]
    A[x]=A[y]
    A[y]=tmp

def trackerAngle():
    grayr = cv2.cvtColor(resr, cv2.COLOR_BGR2GRAY)
    blurredr = cv2.GaussianBlur(grayr, (5, 5), 0)
    threshr = cv2.threshold(blurredr, 100, 255, cv2.THRESH_BINARY)[1]
    edgesr = cv2.Canny(threshr,0,0)
    # find contours in the thresholded image and initialize the
    # shape detector
    cntsr = cv2.findContours(grayr.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cntsr = cntsr[0] if imutils.is_cv2() else cntsr[1]
    sdr = ShapeDetector()
    xr=0
    yr=0
    
    # loop over the contours
    for cr in cntsr:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            flag=1
            M = cv2.moments(cr)
            

            if M["m00"] > 0:
                cXr = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
                cYr = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
                shaper = sd.detect(cr)
                if flag==1:
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                    cr = cr.astype("float")
                    cr *= ratio
                    cr = cr.astype("int")
                    arear=cv2.contourArea(cr)
                    if(arear>100):
                        cv2.drawContours(resized, [cr], -1, (0, 255, 0), 2)
                        cv2.putText(resized, 'red', (cXr, cYr), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
                        cv2.circle(resized,(cXr,cYr),3,(0,255,0),-1)
                        xr=cXr
                        yr=cYr

###########################################################################  GREEN  ##################################################################################################
    grayg = cv2.cvtColor(resg, cv2.COLOR_BGR2GRAY)
    blurredg = cv2.GaussianBlur(grayg, (5, 5), 0)
    threshg = cv2.threshold(blurredg, 50, 255, cv2.THRESH_BINARY)[1]
    edgesg = cv2.Canny(threshg,0,0)
    # find contours in the thresholded image and initialize the
    # shape detector
    cntsg = cv2.findContours(grayg.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cntsg = cntsg[0] if imutils.is_cv2() else cntsg[1]
    sdg = ShapeDetector()
    x1g=0
    x2g=0

    # loop over the contours
    for cg in cntsg:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            flag2=1
            M = cv2.moments(cg)
            

            if M["m00"] > 0:
                cX2g = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
                cY2g = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
                shapeg = sdg.detect(cg)
                if flag2==1:
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                    cg = cg.astype("float")
                    cg *= ratio
                    cg = cg.astype("int")
                    areag=cv2.contourArea(cg)
                    if(areag>100):
                        cv2.drawContours(resized, [cg], -1, (0, 255, 0), 2)
                        cv2.putText(resized, 'green', (cX2g, cY2g), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
                        cv2.circle(resized,(cX2g,cY2g),3,(0,0,255),-1)
                        x1g=cX2g
                        x2g=cY2g
                        
                        
    disth=float(((x1g-xr)*(x1g-xr))+((x2g-yr)*(x2g-yr))^(1/2))
    dista=float(((x1g-x1g)*(x1g-x1g))+((yr-x2g)*(yr-x2g))^(1/2))
    if disth!=0:
        cos = float(dista/disth)
        angle = math.acos(float(cos))
        
        l=round(math.degrees(angle),2)
        if x1g>xr and x2g>yr:
            l=270+l
        elif x1g<xr and x2g>yr:
            quad=3
            l=270-l
        elif x1g<xr and x2g<yr:
            l=l+90
        else:
            l=90-l
        cv2.line(resized,(xr,yr),(x1g,x2g),(255,0,0),2)
    botcx=abs(round((x1g-xr)/2))
    botcy=abs(round((x2g-yr)/2))
    
    cv2.imshow('mask',resized)
##    #cv2.imshow('fme',resbl)
    cv2.waitKey(1)

    return(l,botcx,botcy)
        


cv2.namedWindow('frame')
cv2.createTrackbar('t','frame',0,255,nothing)
cv2.createTrackbar('e1','frame',0,255,nothing)
cv2.createTrackbar('e2','frame',0,1500,nothing)
cv2.namedWindow('frameb')
cv2.createTrackbar('t2','frameb',0,255,nothing)
cv2.createTrackbar('e12','frameb',0,255,nothing)
cv2.createTrackbar('e22','frameb',0,255,nothing)
main_flag_ResTwn=1


while(True):
    if main_flag_ResTwn==True:
        
        # Capture frame-by-frame
        #ret, image = cap.read()
        baseheight = 510
        img = Image.open('arena.jpeg')
        hpercent = (baseheight / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
        img.save('arena2.png')
        image = cv2.imread('arena2.png',1)

        # Our operations on the frame come here
     
        resized = imutils.resize(image, width=690)
        ratio = image.shape[0] / float(resized.shape[0])


        # convert the resized image to grayscale, blur it slightly,
        # and threshold it

        
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
        
        lower_y = np.array([18,87,135])           #YELLOW
        upper_y = np.array([172,195,218])
            
        masky = cv2.inRange(hsv, lower_y, upper_y)
            
        lower_b = np.array([107,143,103])       #brown
        upper_b = np.array([187,180,132])
            
        maskb = cv2.inRange(hsv, lower_b, upper_b)

        lower_bl = np.array([100,43,145])       #blue
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

    ####################################################################    BROWN    ############################################################################################################
        
        gray = cv2.cvtColor(resb, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
##        t = cv2.getTrackbarPos('t','frame')
##        e1 = cv2.getTrackbarPos('e1','frame')
##        e2 = cv2.getTrackbarPos('e2','frame')
        
        thresh = cv2.threshold(blurred, 15, 255, cv2.THRESH_BINARY)[1]
        edges = cv2.Canny(thresh,0,0)
        edgess = imutils.resize(edges, width=690)
        # find contours in the thresholded image and initialize the
        # shape detector
        cnts = cv2.findContours(edgess.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        sd = ShapeDetector()
        area=0
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
                    if(area>40):
                        cv2.drawContours(resized, [c], -1, (0, 255, 0), 2)
                        cv2.putText(resized, ' town hall', (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
                        cv2.circle(resized, (cX, cY),3 , (0, 0, 0), -1)
                  

    ####################################################################      YELLOW   ########################################################################################################

        gray2 = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred2 = cv2.GaussianBlur(gray2, (5, 5), 0)
##        t2 = cv2.getTrackbarPos('t2','frameb')
##        e12 = cv2.getTrackbarPos('e12','frameb')
##        e22 = cv2.getTrackbarPos('e22','frameb')
        thresh2 = cv2.threshold(blurred2, 67, 255, cv2.THRESH_BINARY)[1]
        edges2 = cv2.Canny(thresh2,0,0)
        edgess2= imutils.resize(edges2, width=690)
        # find contours in the thresholded image and initialize the
        # shape detector
        cnts2 = cv2.findContours(edgess2.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts2 = cnts2[0] if imutils.is_cv2() else cnts2[1]
        sd2 = ShapeDetector()
        cyan=255
        k=0
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
                            if(area2>200):   
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
                                ff[k]=2
                                
                                k=k+1
                                cv2.drawContours(resized, [c2], -1, (0, 255, 0), 2)
                                cv2.circle(resized, (cX2, cY2), 3, (0,0,255), -1)
                                cv2.putText(resized,str(qq[k-1]), (cX2, cY2), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
                                cv2.line(resized,(cX,cY),(cX2,cY2),(255,cyan,0),1)
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
    #########################################################################BLUE#####################################################################################################    




        gray3 = cv2.cvtColor(resbl, cv2.COLOR_BGR2GRAY)
        blurred3 = cv2.GaussianBlur(gray3, (5, 5), 0)
        thresh3 = cv2.threshold(blurred3, 0, 255, cv2.THRESH_BINARY)[1]
        edges3 = cv2.Canny(thresh3,0,0)
        edgess3= imutils.resize(edges3, width=690)
        # find contours in the thresholded image and initialize the
        # shape detector
        cnts3 = cv2.findContours(edgess3.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts3 = cnts3[0] if imutils.is_cv2() else cnts3[1]
        sd3 = ShapeDetector()
        area3=[]
        x=[]
        y=[]
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
                
                areab=cv2.contourArea(c3)
                area3.append(areab)
                x.append(cX3)
                y.append(cY3)
        for c3 in cnts3:
            for X in range((x-(area3)**0.5),(x+(area3)**0.5)):
                for Y in range((y-(area3)**0.5),(y+(area3)**0.5)):
                    x.append(X)
                    y.append(Y)

        gridX=570
        gridY=600
        graph=Grid(gridX,gridY)
        img = np.zeros((gridX,gridY,3), np.uint8)
        
        for X in range((x-(area3)**0.5),(x+(area3)**0.5)):
                for Y in range((y-(area3)**0.5),(y+(area3)**0.5)):
                    graph.obstacles = [x,y]
        
                    a_star_search(graph,(cX,cY),(xx,yy),img)
        
                
                    
    
                          
##        x,y,z=trackerAngle()
##        print(x,y,z)
##        main_flag_ResTwn=0
            

###########################################################################  RED ############################################################################################################

# When everything done, release the capture
#cap.release()
cv2.destroyAllWindows()
