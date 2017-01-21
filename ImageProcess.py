##Assign to Akshay
##Functionalities required-
##  capture frame(single image for resource & obsatcle processing)
##  capture video
##  find bot
##  find resources,obstacles,town hall
##  resizing, ratio
import numpy as np
import cv2
import PIL
from PIL import Image
import imutils
from Utils import Utils
from Point import Point
from HSV import Color
from pyimagesearch.shapedetector import ShapeDetector
from Checkpoint import Checkpoint
import math

class Frame(object):
    elements = []
    camera = None
    image = None
    res = None
    ratio = None
    resized = None
    contour = None
    townHall = None  #is of type Checkpoints
    runTimeCounter = 1
    runOnce = True
    @staticmethod
    def connect(cameraID):
        Frame.camera = cv2.VideoCapture(cameraID)
        Frame.camera.set(10,0.5)
        Frame.camera.set(12,255)

    @staticmethod
    def disconnect():
        cv2.VideoCapture.release()

    @staticmethod
    def capture_frame():
        Frame.res, Frame.image = Frame.camera.read()
        Frame.find_ratio()
    @staticmethod
    def show_frame():#
        hsv = cv2.cvtColor(Frame.resized, cv2.COLOR_BGR2HSV)
        res = cv2.bitwise_and(Frame.resized,Frame.resized)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        #cv2.imwrite("frame.jpg", Frame.resized)
        cv2.imshow("frame", Frame.resized)
        cv2.waitKey(5) & 0xFF
    @staticmethod
    def find_ratio():
        Frame.resized = imutils.resize(Frame.image, height=600)
        Frame.ratio = Frame.image.shape[0] / float(Frame.resized.shape[0])
        return Frame.image, Frame.resized, Frame.ratio

    @staticmethod
    def drawCircle(point,color):
        cv2.circle(Frame.resized, point.get_coordinate(), 10 , color, -1)

    @staticmethod
    def processStream(checkpointType):
        hsv = cv2.cvtColor(Frame.resized, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, checkpointType.lower_color.get_array(), checkpointType.upper_color.get_array())
        result = cv2.bitwise_and(Frame.resized, Frame.resized, mask=mask)#TODO figure out why we put the same source for both parameters
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, float(checkpointType.lower_color.T) , 100, cv2.THRESH_BINARY)[1]
        edges = cv2.Canny(thresh,0,0)
        edges_resized = imutils.resize(edges, width=1000)
        #cv2.imshow('edges_resized', edges_resized)
        # find contours in the thresholded image and initialize the
        cnts = cv2.findContours(edges_resized.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour = cnts[0] if imutils.is_cv2() else cnts[1]
        
        #contour =  Frame.find_contour(checkpointType.lower_color.T)
        if(checkpointType.type == "Resource"):
            return Frame.processCheckpoints(contour, checkpointType)
        else:
            return Frame.get_center(contour,checkpointType)

    @staticmethod
    def processCheckpoints(contour,checkpointType):

        cyan = 255
        #orign
        #

        checkPointList = []

        #ShapeDetector
        shapeMessage = None
        for c in contour:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            Moment = cv2.moments(c)
            if Moment["m00"] > 0:

                shapeDetector = ShapeDetector()
                shape = shapeDetector.detect(c)
                position = Point()
                position.x = int((Moment["m10"] / Moment["m00"]+ 1e-7) * Frame.ratio) #uses moment of inertia concept
                position.y = int((Moment["m01"] / Moment["m00"]+ 1e-7) * Frame.ratio)
                
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                
                c = c.astype("float")
                c *= Frame.ratio
                c = c.astype("int")
                area = cv2.contourArea(c)

                display_contour = False
                if area > 1000: 
                    shapeMessage = 'sqr'
                    display_contour = True
                elif  area > 800:
                    shapeMessage = 'trng'
                    display_contour = True
                else:
                    shapeMessage = 'null'
                if display_contour:
                    if(shape == 'circle' or shape == 'square' or shape == 'rectangle' or shape == 'triangle'):
                        if area > 150 :
                            angle = 0
                            
                            origin = Frame.townHall.center
                            #print origin.toString()
                            angle, dist = Utils.angleBetweenPoints(origin,position)
                            Frame.runTimeCounter += 1    
                            
                            checkPointList.append(Checkpoint(area, position, dist, cyan, angle))
                            
                            cv2.drawContours(Frame.resized, [c], -1, checkpointType.contour_color, 2)#cv2.drawContours(source,contours_to_be_passed_as_list,index_of_contours,colour,thickness)
                            cv2.circle(Frame.resized, position.get_coordinate(), 3, (0,0,255), -1)#index_of_contours=>no of contours i guess... -1 means all
                            
                            
                            x,y,w,h = cv2.boundingRect(c)
                            cv2.rectangle(Frame.resized,(x,y),(x+w,y+h),(0,255,0),2)

                            cv2.putText(Frame.resized, shapeMessage + " @" +position.toString() + " | A: "  + str(angle) , position.get_coordinate(), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                            cv2.line(Frame.resized, origin.get_coordinate(), position.get_coordinate(), (255,cyan,0), 2)#draws line from one point ti the other, last arg means thickness
                            cyan = cyan - 1
                            if Frame.runTimeCounter <= 2: 
                                return checkPointList
        #sort checkpoints
        checkPointList.sort()
        return checkPointList
        
    @staticmethod
    def find_contour(threshold):
        #print 'Frame: findContour called '
        gray = cv2.cvtColor(Frame.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 80 , 100, cv2.THRESH_BINARY)[1]
        edges = cv2.Canny(thresh,10,100)
        edges_resized = imutils.resize(edges, width=1000)
        cv2.imshow('contour', edges_resized)
        # find contours in the thresholded image and initialize the
        cnts = cv2.findContours(edges_resized.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        return cnts
    
    @staticmethod
    def draw_contour(contour,contour_name,postion,color):
        cv2.drawContours(Frame.resized, [contour], -1, color, 2)
        cv2.putText(Frame.resized, contour_name, (postion.x, postion.y), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
        cv2.circle(Frame.resized, (postion.x, postion.y),3 , (0, 0, 0), -1)

    @staticmethod
    def get_center(contour,checkpointType):
        #print 'Frame: getCenter called '
        checkPointList = []
        for c in contour:
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            Moment = cv2.moments(c)
            

            if Moment["m00"] > 0:
                origin = None
                if not Frame.runOnce:
                    origin = Frame.townHall.center
                else:
                    origin = Point(0,0)
                Frame.runTimeCounter += 1
                shapeDetector = ShapeDetector()
                shape = shapeDetector.detect(c)
                point = Point()
                point.x = int((Moment["m10"] / Moment["m00"]+ 1e-7) * Frame.ratio)#uses moment of inertia concept
                point.y = int((Moment["m01"] / Moment["m00"]+ 1e-7) * Frame.ratio)
                dist = float((((origin.x-point.x)*(origin.x-point.x))+((origin.y - point.y )*(origin.x - point.y)))^(1/2))
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                #print "Position: " + point.toString()
                c = c.astype("float")
                c *= Frame.ratio
                c = c.astype("int")
                area=cv2.contourArea(c)
                if area > 200:
                    Frame.draw_contour(c,checkpointType.type,point,checkpointType.contour_color)
                    checkPointList.append(Checkpoint(area,point,dist,0,0))
                
        return checkPointList

'''
if __name__ == '__main__':
    Frame.connect(0)
    Frame.cap_frame()
    Frame.find_ratio()
    Frame.show_frame()

    while True:
        Frame.cap_frame()
        Frame.find_ratio()
        Frame.show_frame()
        #cv2.imwrite("frame.jpg", Frame.image)
        #cv2.imshow("frame.jpg", Frame.image)
        #rame.get_center_color("red")


                            if position.x > origin.x and position.y > origin.y:
                                quad = 4
                                angle = 270 + angle
                            elif position.x < origin.x and position.y > origin.y:
                                quad = 3
                                angle = 270 - angle
                            elif position.x < origin.x and position.y < origin.y:
                                quad = 2
                                angle = angle + 90
                            else:
                                quad = 1
                                angle = 90 - angle

        '''