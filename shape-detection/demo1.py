import numpy as np
import cv2
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import PIL
from PIL import Image
import math
import numpy as np
import sys
import urllib2






global cnts
global cnts2
global cntsy

noe=100
xx=np.zeros(shape=(noe))
yy=np.zeros(shape=(noe))
dd=np.zeros(shape=(noe))
cc=np.zeros(shape=(noe))
aa=np.zeros(shape=(noe))
qq=np.zeros(shape=(noe))
ff=np.zeros(shape=(noe))


def bluetoothConnect():
    target_name = "KAIZEN"
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

    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port))

def bluetoothDisconnect():
    sock.close()

def return_to_townhall(char1):
    l,x,y=trackerAngle()
    
    while(TrackerOnTwn(l,x,y)==0):  
        if char1=="f":
            sock.send("b")
            
        elif char1=="r":
            sock.send("l")

        elif char1=="br":
            sock.send("fl")

        elif char1=="b":
            sock.send("f")

        elif char=="bl":
            sock.send("fr")

        elif char=="l":
            sock.send("r")

        elif char=="fl":
            sock.send("br")

        elif char=="fr":
            sock.send("bl")
        l,x,y=trackerAngle()
    sock.send('s')
    sock.send('blink')


def nothing(x):
    pass


def swap(A,x,y):
    tmp = A[x]
    A[x]=A[y]
    A[y]=tmp


def trackerOnRes(a,botcx,botcy):
    k=50
    if((botcx>xx[a]-k and botcx<xx[a]+k)and(botcy>yy[a]-k and botcy<yy[a]+k)) :
        return 1
    else:
        return 0

def TrackerOnTwn(a,botcx,botcy):
    k=50
    if((botcx>townx-k and botcx<townx+k)and(botcy>towny-k and botcy<towny+k)) :
        return 1
    else:
        return 0
           

       
    
def gotores(a,l,x,y):
    u=go_to_direction(l,aa[a])
    return u
def go_to_direction(current_angle,target_ang):    
    if target_ang in range(0,23) or target_ang in range(45,68) or target_ang in range(90,103) or target_ang in range(135,158) or target_ang in range(180,203) or target_ang in range(225,248) or target_ang in range (270,293) or target_ang in range(315,338):
        orientation="clock"
        
        
        if target_ang in range (0,23):
            direction="f"
        elif target_ang in range (45,68):
            direction="fr"
        elif target_ang in range (90,113):
            direction="r"
        elif target_ang in range (135,158):
            direction="br"
        elif target_ang in range (180,203):
            direction="b"
        elif target_ang in range (225,248):
            direction="bl"
        elif target_ang in range (270,293):
            direction="l"
        elif target_ang in range (315,338):
            direction="fl"
                
            
        

    else:
        orientation="aclock"
        
        
        if target_ang in range (23,45):
            direction="fr"
        elif target_ang in range (68,90):
            direction="r"
        elif target_ang in range (113,135):
            direction="br"
        elif target_ang in range (158,180):
            direction="b"
        elif target_ang in range (203,225):
            direction="bl"
        elif target_ang in range (248,270):
            direction="l"
        elif target_ang in range (293,315):
            direction="fl"
        elif target_ang in range (338,360):
            direction="f"

    print(orientation,direction)
    return(orientation,direction)
                
def MainExecute():
    x,y,z=trackerAngle()
    print(x,y,z)
    for n in range(0,18):
        u=gotores(n,x,y,z)
        return_to_twn(u)


def trackerAngle():
    lower_red = np.array([0,132,117])         
    upper_red = np.array([182,195,160])            
    maskred = cv2.inRange(hsv, lower_red, upper_red)
    resred = cv2.bitwise_and(resized,resized, mask= maskred)
    
    grayr = cv2.cvtColor(resred, cv2.COLOR_BGR2GRAY)
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

                        
    lower_gre = np.array([66,92,0])          #green
    upper_gre = np.array([98,255,135])       
    maskgre = cv2.inRange(hsv, lower_gre, upper_gre)
    resgre = cv2.bitwise_and(resized,resized, mask= maskgre)
    grayg = cv2.cvtColor(resgre, cv2.COLOR_BGR2GRAY)
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
    return(l,botcx,botcy)

cv2.namedWindow('frame')
cv2.createTrackbar('t','frame',0,255,nothing)
cv2.createTrackbar('e1','frame',0,255,nothing)
cv2.createTrackbar('e2','frame',0,1500,nothing)
cv2.namedWindow('frameb')
cv2.createTrackbar('t2','frameb',0,255,nothing)
cv2.createTrackbar('e12','frameb',0,255,nothing)
cv2.createTrackbar('e22','frameb',0,255,nothing)



host = "192.168.43.1:8080"
if len(sys.argv)>1:
    host = sys.argv[1]

hoststr = 'http://' + host + '/video'
print 'Streaming ' + hoststr

stream=urllib2.urlopen(hoststr)
flag=1
bytes=''
mainflag=1
townx=0
towny=0                  
while mainflag==1:
    bytes+=stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:] 
        image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)    
        resized = imutils.resize(image, width=875)
        ratio = image.shape[0] / float(resized.shape[0])
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
        
        lower_y = np.array([20,147,95])           #YELLOW
        upper_y = np.array([62,211,204])
            
        masky = cv2.inRange(hsv, lower_y, upper_y)

        lower_gre = np.array([66,92,0])          #green
        upper_gre = np.array([98,255,135])
            
        maskgre = cv2.inRange(hsv, lower_gre, upper_gre)

        lower_red = np.array([0,132,117])          #red
        upper_red = np.array([182,195,160])
            
        maskred = cv2.inRange(hsv, lower_red, upper_red)

        

        res = cv2.bitwise_and(resized,resized, mask= masky)
        resgre = cv2.bitwise_and(resized,resized, mask= maskgre)
        resred = cv2.bitwise_and(resized,resized, mask= maskred)
        
        gray = cv2.cvtColor(resgre, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        t = cv2.getTrackbarPos('t','frame')
        e1 = cv2.getTrackbarPos('e1','frame')
        e2 = cv2.getTrackbarPos('e2','frame')
        
        thresh = cv2.threshold(blurred, 34, 255, cv2.THRESH_BINARY)[1]
        edges = cv2.Canny(thresh,e1,e1)
        edgess = imutils.resize(edges, width=600)
        # find contours in the thresholded image and initialize the
        # shape detector
        cnts = cv2.findContours(edgess.copy(), cv2.RETR_EXTERNAL,
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
                    c = c.astype("float")
                    c *= ratio
                    c = c.astype("int")
                    area=cv2.contourArea(c)
                    if(area>20):
                        cv2.drawContours(resized, [c], -1, (0, 255, 0), 2)
                        cv2.circle(resized, (cX, cY),3 , (0, 0, 0), -1)
                  
        gray2 = cv2.cvtColor(resred, cv2.COLOR_BGR2GRAY)
        blurred2 = cv2.GaussianBlur(gray2, (5, 5), 0)
        thresh2 = cv2.threshold(blurred2, 34, 255, cv2.THRESH_BINARY)[1]
        edges2 = cv2.Canny(thresh2,e1,e1)
        edgess2 = imutils.resize(edges2, width=600)
        # find contours in the thresholded image and initialize the
        # shape detector
        cnts2 = cv2.findContours(edgess2.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts2 = cnts2[0] if imutils.is_cv2() else cnts2[1]
        sd2 = ShapeDetector()
        area2=0
        cX2=0
        cY2=0
        # loop over the contours
        for c2 in cnts2:
                # compute the center of the contour, then detect the name of the
                # shape using only the contour
                M = cv2.moments(c2)
                if M["m00"] > 0:
                    cX2 = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
                    cY2 = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
                    shape = sd2.detect(c2)
                    c2 = c2.astype("float")
                    c2 *= ratio
                    c2 = c2.astype("int")
                    area2=cv2.contourArea(c2)
                    if(area2>20):
                        cv2.drawContours(resized, [c2], -1, (0, 255, 0), 2)
                        cv2.circle(resized, (cX2, cY2),3 , (0, 0, 0), -1)
        townx=int(abs(round((cX2+cX)/2)))
        towny=int(abs(round((cY+cY2)/2)))
                  

        grayy = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurredy = cv2.GaussianBlur(grayy, (5, 5), 0)
        threshy = cv2.threshold(blurredy, 29, 255, cv2.THRESH_BINARY)[1]
        edgesy = cv2.Canny(threshy,0,0)
        edgessy= imutils.resize(edgesy, width=600)
        cntsy = cv2.findContours(edgessy.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cntsy = cntsy[0] if imutils.is_cv2() else cntsy[1]
        sdy = ShapeDetector()
        cyan=255
        k=0
        # loop over the contours
        for cy in cntsy:
                # compute the center of the contour, then detect the name of the
                # shape using only the contour
                M = cv2.moments(cy)
                

                if M["m00"] > 0:
                    cXy = int((M["m10"] / M["m00"]+ 1e-7) * ratio)
                    cYy = int((M["m01"] / M["m00"]+ 1e-7) * ratio)
                    shapey = sdy.detect(cy)
                    
                    # multiply the contour (x, y)-coordinates by the resize ratio,
                    # then draw the contours and the name of the shape on the image
                    cy = cy.astype("float")
                    cy *= ratio
                    cy = cy.astype("int")
                    areay=cv2.contourArea(cy)
                    rat1=(area+area2)/6.25 + 800
                    rat2=(area+area2)/6.25 + 200
                    if(area2>rat2 and area2<rat1):
                        shape3='sqr'
                    elif(area2>(rat2/2) and area2<(rat1/2)+400):
                        shape3='trng'
                    else:
                        shape3='null'
                    if(area2>17):
                        if(shapey=='circle' or shapey=='square' or shapey=='rectangle' or shapey=='triangle'):
                            if(area2>255):   
                                dist2=float((((0.0)*(0.0))+((towny-cYy)*(towny-cYy)))**(0.5))
                                dist=float((((townx-cXy)*(townx-cXy))+((towny-cYy)*(towny-cYy)))**(0.5))
                                sinn=float(dist2/dist)
                                angle = math.acos(float(sinn))
                                j=round(math.degrees(angle),2)
                                if cXy>cX and cYy>cY:
                                    quad=4
                                    j=270+j
                                elif cXy<cX and cYy>cY:
                                    quad=3
                                    j=270-j
                                elif cXy<cX and cYy<cY:
                                    quad=2
                                    j=j+90
                                else:
                                    quad=1
                                    j=90-j
                                
                                xx[k]=cXy
                                yy[k]=cYy
                                dd[k]=dist
                                cc[k]=cyan
                                aa[k]=j
                                qq[k]=quad
                                
                                k=k+1
                                cv2.drawContours(resized, [cy], -1, (0, 255, 0), 2)
                                cv2.circle(resized, (cXy, cYy), 3, (0,0,255), -1)
                                cv2.putText(resized, shape3+'y', (cXy, cYy), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 255), 2)
                                print (townx,towny,cXy,cYy)
                                cv2.line(resized,(townx,towny),(cXy,cYy),(255,cyan,0),2)
                                cyan=cyan-1



        

        for n in range(0,noe):
            for l in range(0,noe-1):
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
                    
                            
        #cv2.imshow('mask',resized)
        k=0
        for n in range(0,noe):
            k=k+1
            if((dd[n]==0)==False):
                break
        dd=dd[k:]
        aa=aa[k:]
        qq=qq[k:]
        cc=cc[k:]
        xx=xx[k:]
        yy=yy[k:]
        ff=ff[k:]
        mainflag=0
        print aa      
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        
l,x,y=trackerAngle()
MainExecute()    
cv2.destroyAllWindows()
