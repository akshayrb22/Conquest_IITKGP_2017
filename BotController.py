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

class BotController(object):
    def __init__(self):
        self.position = Point(0, 0)
        self.angle = 0
    def getPosition(self):
        #assume that you are calling Akshyas Image proccesing function
        Frame.cap_frame()
        contours, point_of_red = Frame.processFrame("red", "BOT T", (0, 0, 255))
        contours, point_of_green = Frame.processFrame("green", "BOT B", (0, 255, 0))

        self.position.x = (point_of_red.x + point_of_green.x) / 2
        self.position.y = (point_of_red.y + point_of_green.y) / 2
    
    def moveforward(self):
        BluetoothController.send_command("f")
        
    def movebackward(self): 
        BluetoothController.send_command("b")
               
    def moveleft(self):
        BluetoothController.send_command("l")

    def moveright(self):
        BluetoothController.send_command("r")

    def moverightForwardDig(self):
        BluetoothController.send_command("rf")

    def moverightBackwardDig(self):
        BluetoothController.send_command("rb")

    def moveleftforwardDig(self):
        BluetoothController.send_command("lf")

    def moveleftBackwardDig(self):
        BluetoothController.send_command("lb")

    def turnantiClockwise(self):
        BluetoothController.send_command("ac")
    
    def turnClockwise(self):
        BluetoothController.send_command("c")



if __name__ == '__main__':
    bot = BotController()
    bot.getPosition()
    BluetoothController.connect()
    print bot.position.toString()
    bot.moveforward()
    raw_input("press")
    
