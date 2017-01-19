from ImageProcess import Frame
from time import sleep
from BotController import BotController
from BluetoothController import BluetoothController
#connect Bluetooth
#BluetoothController.connect()

Frame.connect(0)

Frame.capture_frame()

#bot = BotController()
#bot.getPosition()


Frame.show_frame()
i = 0
while True:
    Frame.capture_frame()
    #redContours,redCenterPoint = Frame.processFrame('yellow',"Yellow",(0,255,0))
    checkPoints = Frame.processResource('yellow',"Res",(0, 0, 150))
    #checkPoints = Frame.processResource("red","Red",(0, 255, 150))

    Frame.show_frame()
    

#for resource in listOfResource
