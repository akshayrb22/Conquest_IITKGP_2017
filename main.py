
# DO NOT CHANGE CODE UNLESS IT IS NECESSARY!!!!! 
# CALL ME IF YOU HAVE ANY DOUBTS!! PHONE no 992075227 :)
# ALL CONFIGURATION OPTIONS ARE AVAILABLE IN Config.py.

# I have not tried updated sorting algorithms!!!!
# If you think this program works, cool. If it doesn't work, that's too bad
# ALL THE BEST :)

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
#sleep(1)
Bot.setBotSpeed(200)
#sleep(1)

Frame.connect(1)
Bot.resource = CheckpointType("Resource", "yellow",(0,255,255))
Bot.obstacle = CheckpointType("Obstacle", "blue",(255,0,0))
Bot.botFront = CheckpointType('botFront', 'green',(0,255,0))
Bot.botBack = CheckpointType('botBack', 'red',(0,0,255))


raw_input("Start ?????? Press Enter to continue.... : ")





Frame.capture_frame()
Frame.townHall = Checkpoint(0,Point(0,0),0,0,0)

#initially find center of townhall by finding bot center
Bot.UpdateProperties()



obstacle_checkPoints = Frame.processStream(Bot.obstacle)
Config.obstacleList = obstacle_checkPoints
Config.obstacleCount = len(obstacle_checkPoints)

#do Astar Search in the beggining
#
resource_checkPoints = Frame.processStream(Bot.resource)
Config.resourceList = resource_checkPoints
if(Config.obstacleCount > 0):
    for resource in resource_checkPoints:
        optimizedAStarPath = AStar.search(Utils.mapPoint(Frame.townHall.center).get_coordinate(), Utils.mapPoint(resource.center).get_coordinate(), Config.mappedWidth, Config.mappedHeight, obstacle_checkPoints)
        distance = Draw.path(optimizedAStarPath)
        finalPath, noOfSkips = Utils.generatePath(Frame.townHall.center, resource.center,optimizedAStarPath)
        resource.path = finalPath
        resource.noOfSkips = noOfSkips
        resource.distance = distance
        print "resource distance " + str(distance)
    #now sort the resources withrespect to the updated distance
    resource_checkPoints.sort()
    #>>>> Call your updated sorting HERE (LEVEL 2)!!!!! Do not change if you dont want to try new algos. 
    # >>>> HERE <<<<<<<      Utils.arena_two_sort(resource_checkPoints)
    #save sorted list
    Config.resourceList = resource_checkPoints
else:
    for resource in resource_checkPoints:
        finalPath, noOfSkips = Utils.generatePath(Frame.townHall.center, resource.center)
        resource.path = finalPath
        resource.noOfSkips = noOfSkips

    #>>>> Call your updated sorting HERE (LEVEL 1)!!!!!
    # >>>> HERE <<<<<<<      Utils.arena_one_sort(resource_checkPoints)


Frame.show_frame()

print "Finished Astar"
## Remove this~!  Only for testing!!!
#sleep(5)

Bot.currentTarget = Checkpoint(0, Point(0, 0), 0, 0, 0)

#initial Run.. covers all resources once (considering only distance)
Bot.Traverse(resource_checkPoints,obstacle_checkPoints)

#call Traverse again with the new sorted resource list

#if you want to travel to Triangles first then squares then use the following sorted
shape_sorted_resource_checkPoints = Utils.prioritySort(resource_checkPoints) # modified prioritySort. please check Source
#if you want to sort using arena_one_sort
#shape_sorted_resource_checkPoints = Utils.arena_one_sort(resource_checkPoints)
Bot.Traverse(shape_sorted_resource_checkPoints,obstacle_checkPoints)
