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
from Checkpoint import Checkpoint
from FindDirectionality import Direction, Orientation
import FindDirectionality
class Bot(object):
    AngleRange = 5
    position = Point(0, 0)
    angle = 0
   
        
    @staticmethod
    def UpdateBotProperties():
        #assume that you are calling Akshay's Image proccesing function
        Frame.capture_frame()
        contours, point_of_red = Frame.processFrame("red", "BOT T", (0, 0, 255))
        contours, point_of_green = Frame.processFrame("green", "BOT B", (0, 255, 0))

        Bot.position.x = (point_of_red.x + point_of_green.x) / 2
        Bot.position.y = (point_of_red.y + point_of_green.y) / 2
        Bot.angle = angle_for_marker(point_of_red, point_of_green)

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
        Bot.UpdateBotProperties()
    @staticmethod
    def changeOrientation(orientation):
        BluetoothController.send_command(Orientation.command[orientation])
        Bot.UpdateBotProperties()



    @staticmethod
    def BackToTownhall(Townhall, ListOfObstacles = None):
        Bot.UpdateBotProperties()
        if Bot.position == Townhall.position:
            Bot.Stop()
            ##TODO wait for some time
        else:
            angle, orientation, direction = get_direction(Townhall.angle)

            while Bot.position != Townhall.position:#TODO make this a range function
                while Bot.angle >= angle + Bot.AngleRange or Bot.angle <= angle + Bot.AngleRange:##receive red_point & green_point parameters
                    Bot.changeOrientation(orientation)
                Bot.moveDirection(direction)
                    ##TODO add the wait function

    @staticmethod
    def Traverse(ListOfResources, ListOfObstacles = None):
    
        for target in ListOfResources:
            Bot.UpdateBotProperties()
            if bot.position == target.position:
                Bot.Stop()
                Bot.Blink()
                ##TODO wait for some time
            else:
                angle, orientation, direction = get_direction(target.angle)
                
                    
                while Bot.position != target.position:#TODO make this a range function
                    while Bot.angle >= angle + Bot.AngleRange or Bot.angle <= angle + Bot.AngleRange:##receive red_point & green_point parameters
                        Bot.changeOrientation(orientation)
                    Bot.moveDirection(direction)
                    ##TODO add the wait function

if __name__ == '__main__':
    BluetoothController.connect()
    Bot.moveDirection(Direction.FORWARD)
    raw_input()
