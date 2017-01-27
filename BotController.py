##Assign to Shreyas
##This is to define the commands which are to be sent to the BluetoothController
##Example-define forward='f'
##Functionalities required-
##  move bot in 8 directions
##  bot stop
##  bot speed control
##  bot orientation (i.e. clock or aclock)
##  should contain the bot class with all it's properties
from Point import Point
from BluetoothController import BluetoothController
from ImageProcess import Frame
from Checkpoint import Checkpoint, CheckpointType, CheckpointShape
import FindDirectionality
from FindDirectionality import Direction, Orientation, MovementFunctions
import FindDirectionality
from Utils import  Utils
from time import sleep,time
import timeit
from AStar import AStar
import copy
import cv2
from Draw import Draw
from Config import Config

class Bot(object):
    
    position = Point(0, 0)
    angle = 0
    botFront = None#CheckpointType('botFront', 'green',(0,255,0))
    botBack = None #CheckpointType('botBack', 'red',(0,0,255))
    resource = None
    prevBack = None
    prevFront = None
    currentTarget = None
    currentResource = None
    currentNode = None
    townHall = None
    runOnce = True
    optimizedAStarPath = None
    currentSpeed = 0
    currentCommand = ''
    
    @staticmethod
    def UpdateProperties():
        Config.startTime = int(timeit.default_timer() * 1000)
        #assume that you are calling Akshay's Image proccesing function
        Frame.capture_frame()
        
        backCheckPointList = Frame.processStream(Bot.botBack)
        frontCheckPointList = Frame.processStream(Bot.botFront)
        
        #print str(Frame.isItMyFirstTime)

        #print "BOT Contours " + str(len(backCheckPointList))  + " , " + str(len(frontCheckPointList))
        if(len(backCheckPointList) <=0 or len(frontCheckPointList)  <= 0):
            print "Failed to Capture bot position !!! >>>>>>>>>>>>>> "
            Bot.moveDirection(Direction.BACKWARD,False)
            #sleep(1)
            Bot.Stop()
        else:
            backCheckPoint = None
            frontCheckPoint = None
            if len(backCheckPointList) > 0 and len(frontCheckPointList) > 0:
                Bot.prevBack = backCheckPointList[0]
                Bot.prevFront = frontCheckPointList[0]
            Bot.position.x = (Bot.prevBack.center.x + Bot.prevFront.center.x) / 2
            Bot.position.y = (Bot.prevBack.center.y + Bot.prevFront.center.y) / 2
            Bot.angle, temp = Utils.angleBetweenPoints(Bot.prevBack.center, Bot.prevFront.center)

            if Bot.runOnce:#Frame.runTimeCounter == 6:
                Frame.townHall = Checkpoint(0,copy.deepcopy(Bot.position),0,0,0)
                Bot.runOnce = False
                Frame.runOnce = False
            else:
                #resource_checkPoints = Frame.processStream(Bot.resource)
                #obstacles_checkPoints = Frame.processStream(Bot.obstacle)
                #TODO Move to ImageProess
                if Config.obstacleBoundingPointList != None:
                    Draw.boundingBox(Config.obstacleBoundingPointList)

                if Bot.currentResource != None:
                    cv2.circle(Frame.resized,Bot.currentResource.center.get_coordinate(),30,(255,150,0),2,8)
                    Draw.circle(Bot.currentResource.path)
                #Frame.drawCircle(Bot.currentTarget.center,(255,0,0))
                if Bot.currentNode != None:
                    cv2.circle(Frame.resized,Bot.currentNode.get_coordinate(),20,(0,0,255),2,4)
                    #Frame.drawCircle(Bot.currentNode,(255,0,0))
                    cv2.putText(Frame.resized, "         Target @" + Bot.currentTarget.center.toString() + " | A: "  + str(Bot.currentTarget.angle) , Bot.currentTarget.center.get_coordinate(), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
                cv2.putText(Frame.resized, "   " + str(Utils.distance(Bot.position,Bot.currentTarget.center)), Utils.midPoint(Bot.position,Bot.currentTarget.center).get_coordinate(), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                if Bot.currentNode != None:
                    cv2.arrowedLine(Frame.resized,Bot.position.get_coordinate(), Bot.currentNode.get_coordinate(), (255,150,0), 2,0,0,0.1)#draws line from one point ti the other, last arg means thickness
                cv2.arrowedLine(Frame.resized,Bot.prevBack.center.get_coordinate(), Bot.prevFront.center.get_coordinate(), (255,255,255), 10,0,0,1)#draws line from one point ti the other, last arg means thickness
                #draw big arrow on top of BOT 
                cv2.arrowedLine(Frame.resized,Bot.prevBack.center.get_coordinate(),Utils.getPointFromAngle(Bot.prevBack.center, Bot.prevFront.center),(255,255,25), 1,0,0,1)
                Frame.drawCircle(Frame.townHall.center,(0,255,255))
                
                if Bot.optimizedAStarPath != None:
                    Draw.path(Bot.optimizedAStarPath)


            #print "Townhall center is:" + str(Frame.townHall.center.toString())
            Frame.drawCircle(Bot.position,(0,255,0))
            cv2.putText(Frame.resized, "           BOT @" +Bot.position.toString() + " | A: "  + str(Bot.angle) , Bot.position.get_coordinate(), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        tempTime = Config.endTime = int(timeit.default_timer() * 1000)

        #show time
        cv2.putText(Frame.resized,"Processing Time : " + str(Config.endTime - Config.startTime), (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(Frame.resized,"Time Elapsed  : " + str(Config.endTime/1000), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        Frame.show_frame()
        Config.endTime = int(timeit.default_timer() * 1000)
        #print "Per frame : " + str((Config.endTime - Config.startTime)) + " | Time elapsed : " + str(Config.endTime/1000)
        return Bot.position, Bot.angle

    @staticmethod
    def Stop():
        BluetoothController.send_command("s")
    @staticmethod
    def Blink():
        BluetoothController.send_command("k")
    
    @staticmethod
    def moveDirection(direction,updateProperties = True):
        #Bot.setBotSpeed(Config.moveSpeed)
        
        if direction == Direction.FORWARD:
            BluetoothController.send_command(Direction.command[direction],"Forward : ^^^^^^^^^^^^^^^^^ ")
        else:
            BluetoothController.send_command(Direction.command[direction],"direction: " + direction)
        if updateProperties == True:
            Bot.UpdateProperties()
    @staticmethod
    def changeOrientation(orientation):
        #Bot.setBotSpeed(Config.turnSpeed)
        if orientation == Orientation.SPOT_LEFT:
            BluetoothController.send_command(Orientation.command[orientation],"Left    : <<<<<<<<<<<<<<<<<") 
        elif orientation == Orientation.SPOT_RIGHT:
            BluetoothController.send_command(Orientation.command[orientation],"Right   : >>>>>>>>>>>>>>>>>")
        else:
            BluetoothController.send_command(Orientation.command[orientation],"orientation: " + orientation)
        Bot.UpdateProperties()

    @staticmethod
    def Traverse(ListOfResources, ListOfObstacles = None):
        print "Townhall center is:" + str(Frame.townHall.center.toString())
        for target in ListOfResources:
            Bot.currentTarget = target
            Bot.currentResource = target
            print " | Target Angle: " + str(Bot.currentTarget.angle)
            Bot.UpdateProperties()
            blinkFlag = 0
           
            #find list of PathPoints to traverse
            # path = Utils.generatePath(Bot.position, Bot.currentTarget.center)
            tempCounter =0
            if target.path != None:
                for node in target.path:
                    #print path
                    Bot.currentNode = node
                    angle, dist = Utils.angleBetweenPoints(Bot.position,node)
                    Bot.currentTarget = Checkpoint(0,node,0,angle,None)

                    firstAdjustLoop = False

                    if Point.inRange(Bot.position, node):
                        print 'Reached Destination  <<<<<<<<<<<<<<<< '
                        Bot.Stop()
                        if (blinkFlag % target.noOfSkips) == (target.noOfSkips-1) & blinkFlag == 1:
                            sleep(0.1)
                            Bot.changeOrientation(Orientation.SPOT_LEFT)
                            print 'BLINKING LED !!!!!!!!!!!!!! '
                            sleep(0.1)
                            Bot.Blink()
                            #sleep(4.6)
                            firstAdjustLoop = True

                        
                    else:
                        while not Point.inRange(Bot.position, node):
                            if firstAdjustLoop != True:
                                Bot.currentTarget.angle, distance = Utils.angleBetweenPoints(Bot.position,Bot.currentTarget.center)
                                if(distance > Config.reduceSpeedAt):
                                    Bot.setBotSpeed(Config.moveSpeed)
                                else:
                                    Bot.setBotSpeed(Utils.map(distance,0, Config.reduceSpeedAt, 100,Config.moveSpeedNear))
                                Bot.moveDirection(Direction.FORWARD)
                                firstAdjustLoop = False
                            tempCounter += 1
                            #print "Distance from center is:" + str(Utils.distance(Bot.position,target.center))
                            while Bot.angle <= (Bot.currentTarget.angle - Config.targetAngleRange) or Bot.angle >= (Bot.currentTarget.angle + Config.targetAngleRange) :##receive red_point & green_point parameters
                                #print " " , (Bot.currentTarget.angle - Config.targetAngelRange) % 360, Bot.angle,  (Bot.currentTarget.angle + Config.targetAngelRange) % 360
                                if Point.inRange(Bot.position, node):
                                    Bot.Stop()
                                    break
                                
                                orientation, speed = Utils.determineTurn(Bot.angle, Bot.currentTarget.angle,Utils.distance(Bot.position,Bot.currentTarget.center))
                                Bot.setBotSpeed(speed)
                                Bot.changeOrientation(orientation)
                                #update bots angle withrespect to target
                                Bot.currentTarget.angle, dist = Utils.angleBetweenPoints(Bot.position,Bot.currentTarget.center)
                                
                    
                    #found the target
                    print 'Reached Destination  >>>>>>>>>> '
                    Bot.Stop()
                    if target.noOfSkips == 1 or (blinkFlag % target.noOfSkips) == target.noOfSkips - 1:
                        sleep(0.1)
                        Bot.changeOrientation(Orientation.SPOT_LEFT)
                        print 'BLINKING LED !!!!!!!!!!!!!! '
                        sleep(0.1)
                        Bot.Blink()

                        # >>>>>>> Value changes for 200 RPM
                        sleep(1)
        print "REACHED ALL DESTINATIONS!!!!!!!!!!!!!!!!!"
        Bot.Stop()
        sleep(100)
    @staticmethod
    def setBotSpeed(speed):
        ##if current speed is different than previous speed, set speed
        
        if speed != Bot.currentSpeed and speed in range(0,256):
            BluetoothController.send_command("X" + str(speed) + "$")
            Bot.currentSpeed = speed

if __name__ == '__main__':
    botFront_green = CheckpointType('botFront', 'green',(0,255,0))
    botBack_red = CheckpointType('botBack', 'red',(0,0,255))
    resourceList = []
    resourceList.append(Checkpoint(0,Point(275,0),0,0,0))
    Bot.UpdateProperties()
    townhall=Checkpoint(0,Bot.position,0,0,0,0)
    BluetoothController.connect()
    Bot.Traverse(resourceList,townhall)
