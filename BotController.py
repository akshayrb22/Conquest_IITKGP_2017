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
from Checkpoint import Checkpoint,CheckpointType
import FindDirectionality
from FindDirectionality import Direction, Orientation,MovementFunctions
import FindDirectionality
from Utils import  Utils
from time import sleep
import copy
import cv2
class Bot(object):
    AngleRange = 180
    position = Point(0, 0)
    angle = 0
    botFront = None#CheckpointType('botFront', 'green',(0,255,0))
    botBack = None #CheckpointType('botBack', 'red',(0,0,255))
    resource = None
    prevBack = None
    prevFront = None
    currentTarget = None
    townHall = None
    runOnce = True
    @staticmethod
    def UpdateProperties():
        #assume that you are calling Akshay's Image proccesing function
        Frame.capture_frame()
        
        backCheckPointList = Frame.processStream(Bot.botBack)
        frontCheckPointList = Frame.processStream(Bot.botFront)
        
        #print str(Frame.isItMyFirstTime)

        #print "BOT Contours " + str(len(backCheckPointList))  + " , " + str(len(frontCheckPointList))
        if(len(backCheckPointList) <=0 or len(frontCheckPointList)  <= 0):
            print "Failed to Capture bot position !!! >>>>>>>>>>>>>> "
        else:
            backCheckPoint = None
            frontCheckPoint = None
            if len(backCheckPointList) > 0 and len(frontCheckPointList) > 0:
                Bot.prevBack = backCheckPointList[0]
                Bot.prevFront = frontCheckPointList[0]
            
            #print "Counter is:" + str(Frame.runTimeCounter)

            Bot.position.x = (Bot.prevBack.center.x + Bot.prevFront.center.x) / 2
            Bot.position.y = (Bot.prevBack.center.y + Bot.prevFront.center.y) / 2
            Bot.angle, temp = Utils.angleBetweenPoints(Bot.prevBack.center, Bot.prevFront.center)
            print "Bot Position:" + Bot.position.toString() + " | Angle: " + str(Bot.angle)
            #sleep(1)
            
            if Bot.runOnce:#Frame.runTimeCounter == 6:
                Frame.townHall = Checkpoint(0,copy.deepcopy(Bot.position),0,0,0)
                Bot.runOnce = False
                Frame.runOnce = False
            else:
                Frame.drawCircle(Bot.currentTarget.center,(255,0,0))
                Frame.drawCircle(Frame.townHall.center,(0,255,255))
                resource_checkPoints = Frame.processStream(Bot.resource)

            #print "Townhall center is:" + str(Frame.townHall.center.toString())
            Frame.drawCircle(Bot.position,(0,255,0))
            cv2.putText(Frame.resized, " BOT @" +Bot.position.toString() + " | A: "  + str(Bot.angle) , Bot.position.get_coordinate(), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

        Frame.show_frame()
        return Bot.position, Bot.angle

    @staticmethod
    def turnAntiClockwise():
        BluetoothController.send_command("ac")
    @staticmethod
    def turnClockwise():
        BluetoothController.send_command("c")
    @staticmethod
    def Stop():
        BluetoothController.send_command("s")
    @staticmethod
    def Blink():
        BluetoothController.send_command("blink")
    @staticmethod
    def moveDirection(direction):
        #BluetoothController.send_command(Direction.command[direction])

        print "direction: " + direction
        sleep(0.1)
        Bot.Stop()
        Bot.UpdateProperties()
    @staticmethod
    def changeOrientation(orientation):
        #BluetoothController.send_command(Orientation.command[orientation])

        print "orientation: " + orientation
        sleep(0.1)

        Bot.UpdateProperties()
        #return Bot.position, Bot.angle
    @staticmethod
    def BackToTownhall(ListOfObstacles = None):
        Bot.UpdateProperties()
        if Point.inRange(Bot.position, Bot.townHall.center):
            Bot.Stop()
            sleep(1)
        else:
            angle, orientation, direction = get_direction((Bot.currentTarget.angle + 180) % 360)

            while not Point.inRange(Bot.position, Bot.townHall.position):
                print "Turning ######"
                while Bot.angle >= angle - Bot.AngleRange or Bot.angle <= angle + Bot.AngleRange:##receive red_point & green_point parameters
                    Bot.position,Bot.angle = Bot.changeOrientation(orientation)
                print "Moving##########"
                Bot.moveDirection(direction)
            Bot.Stop()      
    @staticmethod
    def Traverse(ListOfResources, ListOfObstacles = None):
        print "Townhall center is:" + str(Frame.townHall.center.toString())
        for target in ListOfResources:
            Bot.currentTarget = target
            print " | Target Angle: " + str(Bot.currentTarget.angle)
            Bot.UpdateProperties()
            if Point.inRange(Bot.position, target.center):
                Bot.Stop()
                Bot.Blink()
                sleep(10)
                Bot.Stop()
            else:
                angle, orientation, direction = MovementFunctions.get_direction(target.angle)

                while not Point.inRange(Bot.position, target.center):
                    print "Distance from center is:" + str(Utils.distance(Bot.position,target.center))
                    while Bot.angle >= target.angle - Bot.AngleRange or Bot.angle <= target.angle + Bot.AngleRange:##receive red_point & green_point parameters
                        print "Bot angle:" + str(Bot.angle)
                        print "target angle:" + str(target.angle)
                        if Bot.angle - target.angle < 0:
                            Bot.changeOrientation(Orientation.CLOCKWISE) 
                        else:
                            Bot.changeOrientation(Orientation.ANTI_CLOCKWISE)

                        #Bot.changeOrientation(orientation) 
                    Bot.moveDirection(MovementFunctions.get_direction(angle_of_resource))
                Bot.Stop()
                Bot.Blink()
                print 'Reached Destination  >>>>>>>>>> '
                sleep(10)
                BluetoothController.send_command("stop")
            Bot.BackToTownhall(ListOfObstacles = None)
            
                ##TODO wait for some time
if __name__ == '__main__':
    botFront_green = CheckpointType('botFront', 'green',(0,255,0))
    botBack_red = CheckpointType('botBack', 'red',(0,0,255))
    resourceList = []
    resourceList.append(Checkpoint(0,Point(275,0),0,0,0))
    Bot.UpdateProperties()
    townhall=Checkpoint(0,Bot.position,0,0,0,0)
    BluetoothController.connect()
    Bot.Traverse(resourceList,townhall)
