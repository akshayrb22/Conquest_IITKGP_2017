from ImageProcess import Frame
from time import sleep
from BotController import BotController
from BluetoothController import BluetoothController
#connect Bluetooth
BluetoothController.connect()

Frame.connect(1)

Frame.cap_frame()
Frame.find_ratio()

bot = BotController()
#bot.getPosition()

#redContours,redCenterPoint = Frame.processFrame("red","Town Hall",(0,255,0))
#listOfResource = Frame.processResource("yellow","Res",(0,0,255))
Frame.show_frame()
i = 0
while True:
    Frame.cap_frame()
    Frame.find_ratio()
    redContours,redCenterPoint = Frame.processFrame("yellow","Yellow",(0,255,0))
    #redContours,redCenterPoint = Frame.processFrame("red","Red",(0,255,0))
    #position = bot.getPosition()
    #print "Red Center : " + str(position.get_coordinate())
    Frame.show_frame()
    #sleep(0.5)


#for resource in listOfResource
