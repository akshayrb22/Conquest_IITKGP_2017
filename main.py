import math
from time import sleep

import cv2
from Area import Area
from AStar import *
from BluetoothController import BluetoothController
from BotController import Bot
from Checkpoint import Checkpoint, CheckpointType
from ImageProcess import Frame
from Point import Point

#connect Bluetooth
BluetoothController.connect()
Bot.Stop()
sleep(1)
Bot.setBotSpeed(40)
sleep(1)

Frame.connect(1)
Bot.resource = CheckpointType("Resource", "yellow",(0,255,255))
Bot.obstacle = CheckpointType("Obstacle", "purple",(255,0,0))
Bot.botFront = CheckpointType('botFront', 'green',(0,255,0))
Bot.botBack = CheckpointType('botBack', 'red',(0,0,255))


Frame.capture_frame()
Frame.townHall = Checkpoint(0,Point(0,0),0,0,0)

#initially find center of townhall by finding bot center
Bot.UpdateProperties()


obstacle_checkPoints = Frame.processStream(Bot.obstacle)
Config.obstacleCount = len(obstacle_checkPoints)

#do Astar Search in the beggining
#
resource_checkPoints = Frame.processStream(Bot.resource)
if(Config.obstacleCount > 0):
    for resource in resource_checkPoints:
        optimizedAStarPath = AStar.search(Utils.mapPoint(Frame.townHall.center).get_coordinate(), Utils.mapPoint(resource.center).get_coordinate(), Config.mappedWidth, Config.mappedHeight, obstacle_checkPoints)
        distance = Draw.path(optimizedAStarPath)
        finalPath, noOfSkips = Utils.generatePath(Frame.townHall.center, resource.center,optimizedAStarPath)
        resource.path = finalPath
        resource.noOfSkips = noOfSkips
        resource.distance = distance
        #now sort the resources withrespect to the updated distance
        resource_checkPoints.sort()
    Config.obstacleList = resource_checkPoints
else:
    for resource in resource_checkPoints:
        finalPath, noOfSkips = Utils.generatePath(Frame.townHall.center, resource.center)
        resource.path = finalPath
        resource.noOfSkips = noOfSkips



Config.findPathOnce = False

Bot.currentTarget = Checkpoint(0, Point(0, 0), 0, 0, 0)

Bot.Traverse(resource_checkPoints,obstacle_checkPoints)
