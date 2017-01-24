from ImageProcess import Frame
from time import sleep
from BluetoothController import BluetoothController
from Checkpoint import CheckpointType, Checkpoint
from Area import Area
from Point import Point
import math
from BotController import Bot
import cv2
from AStar import *



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


Frame.townHall = Checkpoint(0,Point(0,0),0,0,0)

#initially find center of townhall by finding bot center
Bot.UpdateProperties()

resource_checkPoints = Frame.processStream(Bot.resource)

obstacle_checkPoints = Frame.processStream(Bot.obstacle)

Bot.currentTarget = Checkpoint(0, Point(0, 0), 0, 0, 0)

Bot.Traverse(resource_checkPoints,obstacle_checkPoints)