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
class Bot(object):
    AngleRange = 5
    position = Point(0, 0)
    angle = 0
    @staticmethod
    def UpdateProperties():
        #assume that you are calling Akshay's Image proccesing function
        #Frame.capture_frame()
        redCheckPoint = Checkpoint(0,Point(275,275),0,0,0,0) #Frame.processStream(botBack_red)[0]
        greenCheckPoint = Checkpoint(0,Point(275,300),0,0,0,0) # Frame.processStream(botFront_green)[0]

        Bot.position.x = (redCheckPoint.center.x + greenCheckPoint.center.x) / 2
        Bot.position.y = (redCheckPoint.center.y + greenCheckPoint.center.y) / 2
        Bot.angle = Utils.angleBetweenPoints(redCheckPoint.center, greenCheckPoint.center)
        print "Bot Position:" + Bot.position.toString() + " | Angle: " + str(Bot.angle)
        sleep(1)
        return Bot.position, Bot.angle

    @staticmethod
    def turnAntiClockwise():
        BluetoothController.send_command("ac")
    @staticmethod
    def turnClockwise():
        BluetoothController.send_command("c")
    @staticmethod
    def Stop():
        BluetoothController.send_command("Stop")
    @staticmethod
    def Blink():
        BluetoothController.send_command("Blink")
    @staticmethod
    def moveDirection(direction):
        BluetoothController.send_command(Direction.command[direction])
        Bot.UpdateProperties()
        print "direction" + direction
    @staticmethod
    def changeOrientation(orientation):
        BluetoothController.send_command(Orientation.command[orientation])
        Bot.UpdateProperties()
        print "orientation: " + orientation


    @staticmethod
    def BackToTownhall(townhallPosition, ListOfObstacles = None):
        Bot.UpdateProperties()
        if Bot.position == townhallPosition:
            Bot.Stop()
            ##TODO wait for some time
        else:
            angle, orientation, direction = get_direction(Townhall.angle)

            while Bot.position != Townhall.position:#TODO make this a range function
                while Bot.angle >= angle + Bot.AngleRange or Bot.angle <= angle + Bot.AngleRange:##receive red_point & green_point parameters
                    Bot.changeOrientation(orientation)
                Bot.moveDirection(direction)
                    ##TODO add the wait function
            Bot.Stop()      
    @staticmethod
    def Traverse(ListOfResources, townhall, ListOfObstacles = None):
        
        for target in ListOfResources:
            Bot.UpdateProperties()
            if Bot.position == target.center:
                Bot.Stop()
                Bot.Blink()
                ##TODO wait for some time
            else:
                angle, orientation, direction = MovementFunctions.get_direction(target.angle)
                
                    
                while Bot.position != target.center:#TODO make this a range function
                    while Bot.angle >= angle + Bot.AngleRange or Bot.angle <= angle + Bot.AngleRange:##receive red_point & green_point parameters
                        Bot.changeOrientation(orientation)
                    Bot.moveDirection(direction)
                    ##TODO add the wait function
                Bot.Stop()
                Bot.Blink()
            BackToTownhall(townhall, ListOfObstacles = None)
            
                ##TODO wait for some time
if __name__ == '__main__':
    botFront_green = CheckpointType('botFront', 'green',(0,255,0))
    botBack_red = CheckpointType('botBack', 'red',(0,0,255))
    resourceList = []
    resourceList.append(Checkpoint(0,Point(275,0),0,0,0,0))
    Bot.UpdateProperties()
    townhall=Checkpoint(0,Bot.position,0,0,0,0)
    BluetoothController.connect()
    Bot.Traverse(resourceList,townhall)
