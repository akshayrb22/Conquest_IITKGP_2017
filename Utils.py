##Open to everyone
##Any person who creates a helper function can place it here
##After adding a function please menrion it in the intital comments
##Contains-
##  Angle for marker()
##  distance formula()

import copy
from math import *

import numpy as np

from Checkpoint import Checkpoint, CheckpointShape
from Config import Config
from FindDirectionality import *
from Point import Point


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
        '''
        param-origin [Type-Point], position [Type-Point]
        returns-angleInDegrees [Type-float], dist [Type-float]
        Uses simple tan inverse function to find hte angle then maps it to a proper angle between 0 to 360.
        '''
        
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
    def determineTurn(botAngle, targetAngle, distance): #TODO fix it !
        '''
        param-botAngle [Type-float], targetAngle [Type-float], distance [Type-float]
        returns-Orientation.orientation [Type-str], Config.turnSpeed [Type-int]
        This function decides the direction with which the bot should turn and the speed with which it should do it.
        '''
        deltaAngle = botAngle - targetAngle

        if deltaAngle >= 180:
            deltaAngle -= 360
        deltaAngle %= 360
        absDeltaAngle = abs(deltaAngle)

        mappedAngle = 30 # DECREASE THIS IF YOU WANT FAST SPOT TURN @ Node

        if deltaAngle >= 180:
            if absDeltaAngle > mappedAngle:
                return Orientation.SPOT_LEFT, Config.turnSpeed 
            elif distance > 120:
                return Orientation.ARC_LEFT, Config.turnSpeed
            else :
                return Orientation.SPOT_LEFT, Config.turnSpeed - 60
        else:
            if absDeltaAngle > mappedAngle :
                return Orientation.SPOT_RIGHT, Config.turnSpeed
            elif  distance > 120:
                return Orientation.ARC_RIGHT, Config.turnSpeed
            else:
                return Orientation.SPOT_RIGHT, Config.turnSpeed - 60
       
    @staticmethod
    def generatePath(botPosition, targetPosition, aStarPath=None):
        '''
        param-botPosition [Point object], targetPosition [Point object], aStarPath [list of Point objects, default = None]
        returns-finalPath [Type-list of Point objects], noOfSkips [Type-int]
        If there are obstacles, the obstacle points are added to the path list, otherwise i.e.if it is in t he first round,
        there are only 2 points considered, the townhall and the resource point.
        '''
        finalPath = []

        #path for FirstPass
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
        #if go to resource twice
        if Config.goToResourceTwice == True:
            del firstPass[0]
            finalPath += copy.deepcopy(firstPass)

        del finalPath[0]
        return finalPath, noOfSkips
    
    @staticmethod
    def prioritySort(checkPointList):
        '''
        param:checkPointList [Type-list of Checkpoint objects, here resources]
        returns- priorityResources [Type-list of Checkpoint objectS, here resources ]
        This function is one that can be called once the first run is done. 
        It just goes for the triangles as they carry more points

        '''
        priorityResources = []
        skippedResources = []
        for j in range (len(checkPointList)-1):
            if checkPointList[j].shape == CheckpointShape.TRIANGLE:
                priorityResources.append(checkPointList[j])
            else:
                skippedResources.append(checkPointList[j]) #keep all Square resources to add at the end
        priorityResources += copy.deepcopy(skippedResources)
        return priorityResources
    
if __name__ == '__main__':
    checkPointList = []
    checkPointList.append(Checkpoint(800,Point(10,10),100,0,CheckpointShape.SQUARE))
    checkPointList.append(Checkpoint(800,Point(10,10),190,0,CheckpointShape.SQUARE))
    checkPointList.append(Checkpoint(960,Point(400,200),370,0,CheckpointShape.TRIANGLE))
    checkPointList.append(Checkpoint(1000,Point(100,60),4566,0,CheckpointShape.TRIANGLE))
    checkPointList.append(Checkpoint(800,Point(10,10),5000,0,CheckpointShape.SQUARE))
    checkPointList.append(Checkpoint(960,Point(400,200),9000,0,CheckpointShape.TRIANGLE))
    checkPointList = Utils.prioritySort(checkPointList)
    for i in checkPointList:
        print i.shape,i.distance
    #print Utils.generatePath((0,0),(10,10),[(0,0),(9,9),(13,12)])
    # turn = Utils.determineTurn3(180, 0)    
    # print turn
