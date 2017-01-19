from ImageProcess import Frame
from time import sleep
#from BotController import BotController
from BluetoothController import BluetoothController
from Checkpoint import CheckpointType
from Area import Area
#connect Bluetooth
#BluetoothController.connect()

Frame.connect(1)

Frame.capture_frame()

#bot = BotController()
#bot.getPosition()
#todo get the min, max values

resource = CheckpointType("Resource", "yellow",(0,255,255))
#obstacle = CheckpointType("Obstacle", "blue")
botFront_green = CheckpointType('botFront', 'green',(0,255,0))
botBack_red = CheckpointType('botBack', 'red',(0,0,255))


while True:
    Frame.capture_frame()
    resource_checkPoints = Frame.processStream(resource)
    #obstacle_checkPoints = Frame.processStream(obstacle)
    botFront_green_checkPoints = Frame.processStream(botFront_green)
    botBack_red_checkPoints = Frame.processStream(botBack_red)


    Frame.show_frame()   

#for resource in listOfResource

