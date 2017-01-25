##Open to everyone
##Any person who creates a helper function can place it here
##After adding a function please menrion it in the intital comments
##Contains-
##  Angle for marker()
##  distance formula()

from math import *
import numpy as np
from Point import Point
import copy
from FindDirectionality import *
from Checkpoint import Checkpoint,CheckpointShape
from Config import Config
class Utils(object):
    @staticmethod
    def arena_one_sort(checkPointList):
        for j in range(0,len(checkPointList)-1):
            if ((checkPointList[j].distance > (checkPointList[j+1].distance)/2) and (checkPointList[j].shape ==  CheckpointShape.SQUARE and checkPointList[j+1].shape == CheckpointShape.TRIANGLE)):
                checkPointList[j],checkPointList[j+1]=checkPointList[j+1],checkPointList[j]
        return checkPointList

    @staticmethod
    def arena_two_sort(checkPointList):
        if (checkPointList[0].shape == checkPointList[1].shape):
            if checkPointList[0].shape== Checkpoint:
                for i in range(len(checkPointList)):
                    if checkPointList[i].shape== CheckpointShape.TRIANGLE:
                        deleted_element = checkPointList.pop(i)
                        checkPointList.reverse()
                        checkPointList.append(deleted_element)                  
                        checkPointList.reverse()
                        break
            elif checkPointList[0].shape== CheckpointShape.TRIANGLE:
                for i in range(len(checkPointList)):
                    if checkPointList[i].shape== CheckpointShape.SQUARE:
                        deleted_element = checkPointList.pop(i)
                        checkPointList.reverse()
                        checkPointList.append(deleted_element)                  
                        checkPointList.reverse()
                        break
        return checkPointList



    @staticmethod
    def angleBetweenPoints(origin,position):
        
        deltaY = position.y - origin.y
        deltaX = position.x - origin.x
        angleInDegrees = round(atan2(deltaY, deltaX) * float(180) / 3.14)
        if angleInDegrees < 0: 
            #angle is in I and II Quad, ie between 0 to -180, so map it to 0,180
            angleInDegrees = Utils.map(angleInDegrees,0,-180,0,180)
        else:
            #angle is in III and IV Quad, ie between 0 to -180, so map it to 360,180
            angleInDegrees = Utils.map(angleInDegrees,0,180,360,180)
        return angleInDegrees, Utils.distance(origin, position)

    @staticmethod
    def distance(pt1,pt2):
        dist = round(sqrt(((pt1.x-pt2.x)*(pt1.x-pt2.x))+((pt1.y-pt2.y)*(pt1.y-pt2.y))))
        return dist
    @staticmethod
    def map(value, in_min, in_max, out_min, out_max):
        return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    
    @staticmethod
    def mapPoint(point):
        x = Utils.map(point.x, 0, Config.FrameWidth,0,Config.mappedWidth)
        y = Utils.map(point.y,0,Config.FrameHeight,0,Config.mappedHeight)
        return Point(x,y)
    @staticmethod
    def remapPoint(point):
        x = Utils.map(point.x, 0, Config.mappedWidth,0,Config.FrameWidth)
        y = Utils.map(point.y,0,Config.mappedHeight,0,Config.FrameHeight)
        return Point(x,y)

    @staticmethod
    def midPoint(point1,point2):
        return Point((point1.x + point2.x)/2,(point1.y + point2.y)/2)
    @staticmethod
    def getQuadrant(angle):
        if angle in range(0, 91): return 1
        if angle in range(91, 181): return 2
        if angle in range(181, 271): return 3
        if angle in range(271, 360): return 4    

    @staticmethod
    def getPointFromAngle(p1,p2):
        x=(101*p2.x)-(p1.x*100)
        y=(101*p2.y)-(p1.y*100)
        return (x,y)

    @staticmethod
    def determineTurn(botAngle, targetAngle,distance): #TODO fix it !
        deltaAngle = botAngle - targetAngle

        if deltaAngle >= 180:
            deltaAngle -= 360
        deltaAngle %= 360
        absDeltaAngle = abs(deltaAngle)

        mappedAngle = 25 #Utils.map(distance,0,500,0,25)
        #print " angle " + str(deltaAngle) + " distance " + str(distance) + " mappedAngle " + str(mappedAngle)

        if deltaAngle >= 180:
            if absDeltaAngle > mappedAngle and distance < 50:
                return Orientation.ARC_LEFT
            else:
                return Orientation.SPOT_LEFT
        else:
            if absDeltaAngle > mappedAngle  and distance < 50:
                return Orientation.ARC_RIGHT
            else:
                return Orientation.SPOT_RIGHT
        
    @staticmethod
    def generatePath(botPosition, targetPosition, aStarPath=None):
        finalPath = []

        #path for FirstPast
        firstPass = []
        pathToTarget = []
        if aStarPath != None:
            for point in aStarPath:
                pathToTarget.append(Point(int(point[0]),int(point[1])))#+= copy.deepcopy(aStarPath)
            pathToTarget[len(pathToTarget) - 1 ] = targetPosition
        else:
            pathToTarget = []
            pathToTarget.append(botPosition) #botPosition
            pathToTarget.append(targetPosition) #target Position
        noOfSkips = len(pathToTarget) - 1
        firstPass += copy.deepcopy(pathToTarget) #from bot postion to target
        #delete target from reversed pathToTarget
        del pathToTarget[len(pathToTarget) - 1]
        pathToTarget.reverse()
        firstPass += copy.deepcopy(pathToTarget)

        finalPath += copy.deepcopy(firstPass)       
        del firstPass[0]
        finalPath += copy.deepcopy(firstPass)

        del finalPath[0]
        return finalPath, noOfSkips
    
    
if __name__ == '__main__':
    checkPointList = []
    checkPointList.append(Checkpoint(800,Point(10,10),100,0,CheckpointShape.SQUARE))
    checkPointList.append(Checkpoint(800,Point(10,10),190,0,CheckpointShape.SQUARE))
    checkPointList.append(Checkpoint(960,Point(400,200),370,0,CheckpointShape.TRIANGLE))
    checkPointList.append(Checkpoint(1000,Point(100,60),4566,0,CheckpointShape.TRIANGLE))
    checkPointList.append(Checkpoint(800,Point(10,10),5000,0,CheckpointShape.SQUARE))
    checkPointList.append(Checkpoint(960,Point(400,200),9000,0,CheckpointShape.TRIANGLE))
    checkPointList = Utils.arena_two_sort(checkPointList)
    for i in checkPointList:
        print i.shape,i.distance
    # turn = Utils.determineTurn3(180, 0)    
    # print turn