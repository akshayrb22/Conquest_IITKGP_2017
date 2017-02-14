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
from Checkpoint import Checkpoint,CheckpointShape
from Config import Config
import math


class Frame(object):
    width = None
    height = None

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
    botPosition = None
    @staticmethod
    def connect(cameraID):
        Frame.camera = cv2.VideoCapture(cameraID)
        Frame.camera.set(10,0.5)#brightness
        Frame.camera.set(12,255)#saturation
        Frame.camera.set(5,18) #frame rate
        Frame.camera.set(21,1) #buffer Size

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
        Frame.width = Frame.resized.shape[1]
        Frame.height = Frame.resized.shape[0]
        Config.FrameWidth = Frame.width
        Config.FrameHeight = Frame.height
        return Frame.image, Frame.resized, Frame.ratio

    @staticmethod
    def drawCircle(point,color):
        cv2.circle(Frame.resized, point.get_coordinate(), 10 , color, -1)
    
    @staticmethod
    def processStream(checkpointType):
        ''''
        param- checkpointType [Type-CheckpointType object]
        returns-if resource Frame.processCheckpoints(contour, checkpointType)->checkPointList [Type-list of resource or
                obstacle Checkpoint] else Frame.processBot(contour,checkpointType)->checkPointList[Type-list of bot checkpoint]
        It converts the color of the frame to hsv, then it masks it, grays it, threshes, gets the canny image first and then 
        resizes it. After all this, we get the contours and based on if the checkpoint type is a resource or an obstacle and 
        if it is a bot property, a function is called and returned.
        '''
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
            return Frame.processBot(contour,checkpointType)
    
    @staticmethod
    def processCheckpoints(contour,checkpointType):
    '''
    param-contour [Type-list], checkpointType[Type-CheckpointType object]
    returns-checkPointList[Type-list of Checkpoint objects]
    I have commented the cyan lines as we don't use them in the final code.
    After initializing a checkpointlist array, we get the center of each contour and then based on the 
    area we decide if the checkpoint is a tringle or a square
    Then we append them to the list
    If it is a resource, it is both triangles and squares  and the final list is sorted according to area so the
    triangles come first. If it is an obstacle we need only consider squares.
    '''

        #cyan = 255
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
                if area > 600: 
                    shapeMessage = 'square'
                    shape = CheckpointShape.SQUARE
                    display_contour = True
                elif  area > 400:
                    shapeMessage = 'triangle'
                    shape = CheckpointShape.TRIANGLE
                    display_contour = True
                else:
                    shapeMessage = 'null'
                if display_contour:
                    if(shape == CheckpointShape.SQUARE or shape == CheckpointShape.TRIANGLE):
                        #if area > 310 :#this is a boiler plate
                        angle = 0
                        
                        origin = Frame.townHall.center
                        #print origin.toString()
                        angle, dist = Utils.angleBetweenPoints(origin,position)
                        Frame.runTimeCounter += 1    
                        

                        
                        checkPointList.append(Checkpoint(area, position, dist, angle, shape))
                        
                        cv2.drawContours(Frame.resized, [c], -1, checkpointType.contour_color, 2)#cv2.drawContours(source,contours_to_be_passed_as_list,index_of_contours,colour,thickness)
                        cv2.circle(Frame.resized, position.get_coordinate(), 3, (0,0,255), -1)#index_of_contours=>no of contours i guess... -1 means all
                        
                        
                        x,y,w,h = cv2.boundingRect(c)
                        cv2.rectangle(Frame.resized,(x,y),(x+w,y+h),(0,255,0),2)

                        #cv2.putText(Frame.resized, shapeMessage + " @" +position.toString() + " | A: "  + str(angle) , position.get_coordinate(), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                        #cv2.line(Frame.resized, origin.get_coordinate(), position.get_coordinate(), (255,cyan,0), 2)#draws line from one point ti the other, last arg means thickness
                        #cyan = cyan - 1
                        #if Frame.runTimeCounter <= 2: 
                        #    return checkPointList
        #sort checkpoints
        checkPointList.sort()
        return checkPointList
    #has been defined, never used
    ''''    
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
    '''
    @staticmethod
    def draw_contour(contour,contour_name,postion,color):
        cv2.drawContours(Frame.resized, [contour], -1, color, 2)
        #cv2.putText(Frame.resized, contour_name, (postion.x, postion.y), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
        cv2.circle(Frame.resized, (postion.x, postion.y),3 , (0, 0, 0), -1)
    
    @staticmethod
    def processBot(contour,checkpointType):
    '''
    param-contour [Type-list], checkpointType[Type-CheckpointType object]
    returns-checkPointList[Type-list of Checkpoint objects]
    It works the same way as Frame.processCheckpoints(). The exact same way as above.  
    ''' 
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
                #shape = shapeDetector.detect(c)
                shape = CheckpointShape.SQUARE
                #print "DEtected Shape " + shape
                point = Point()
                point.x = int((Moment["m10"] / Moment["m00"]+ 1e-7) * Frame.ratio)#uses moment of inertia concept
                point.y = int((Moment["m01"] / Moment["m00"]+ 1e-7) * Frame.ratio)
                dist = float(distance(origin,point))
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                #print "Position: " + point.toString()
                c = c.astype("float")
                c *= Frame.ratio
                c = c.astype("int")
                area=cv2.contourArea(c)
                if area > 1600:
                    Frame.draw_contour(c,checkpointType.type, point, checkpointType.contour_color)
                    checkPointList.append(Checkpoint(area, point, dist, 0, shape))
                
        return checkPointList
    
    @staticmethod
    def botImageProperties(botCurrentResource, botCurrentNode, botCurrentTarget, botPrevBack, botPrevFront, botPosition):
    '''
    param-botCurrentResource [Type-Checkpoint object], botCurrentNode [Type-Checkpoint object],
          botCurrentTarget [Type-Checkpoint object], botPrevBack [Type-Checkpoint object], 
          botPrevFront [Type-Checkpoint object], botPosition [Type-Checkpoint object]
    returns-None
    It does some image processing. It draws the bounding boxes for the obstacles, the point on the current resource
    that our bot has to traverse to. It draws a circle on the node that it has to reach. It also gives the target angle 
    in real time on the screen. It draws line from one point to the other, last arg means thickness. It draws arrowed 
    lines as well.
    '''
        if Config.obstacleBoundingPointList != None:
            Draw.boundingBox(Config.obstacleBoundingPointList)
        if botCurrentResource != None:
            cv2.circle(Frame.resized,botCurrentResource.center.get_coordinate(),30,(255,150,0),2,8)
            Draw.circle(botCurrentResource.path)
        #Frame.drawCircle(Bot.currentTarget.center,(255,0,0))
        if botCurrentNode != None:
            cv2.circle(Frame.resized,botCurrentNode.get_coordinate(),20,(0,0,255),2,4)
            #Frame.drawCircle(Bot.currentNode,(255,0,0))
            cv2.putText(Frame.resized, "         Target @" + botCurrentTarget.center.toString() + " | A: "  + str(botCurrentTarget.angle) , botCurrentTarget.center.get_coordinate(), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
        cv2.putText(Frame.resized, "   " + str(Utils.distance(botPosition,botCurrentTarget.center)), Utils.midPoint(botPosition,botCurrentTarget.center).get_coordinate(), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        if botCurrentNode != None:
            cv2.arrowedLine(Frame.resized,botPosition.get_coordinate(), botCurrentNode.get_coordinate(), (255,150,0), 2,0,0,0.1)#draws line from one point ti the other, last arg means thickness
        cv2.arrowedLine(Frame.resized,botPrevBack.center.get_coordinate(), botPrevFront.center.get_coordinate(), (255,255,255), 10,0,0,1)#draws line from one point ti the other, last arg means thickness
        #draw big arrow on top of BOT 
        cv2.arrowedLine(Frame.resized,botPrevBack.center.get_coordinate(),Utils.getPointFromAngle(botPrevBack.center, botPrevFront.center),(255,255,25), 1,0,0,1)
        Frame.drawCircle(Frame.townHall.center,(0,255,255)) 
   

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