from ImageProcess import Frame
from time import sleep
from BotController import BotController
#connect Bluetooth
#BluetoothController.connect()

Frame.connect(0)

Frame.cap_frame()
Frame.find_ratio()

bot = BotController()
bot.getPosition()

redContours,redCenterPoint = Frame.processFrame("red","Town Hall",(0,255,0))
listOfResource = Frame.processResource("yellow","Res",(0,0,255))
Frame.show_frame()
i = 0
while True:
    Frame.cap_frame()
    Frame.find_ratio()
    Frame.show_frame()


#for resource in listOfResource
