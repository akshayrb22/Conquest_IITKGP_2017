from ImageProcess import Frame
from BluetoothController import BluetoothController

#connect Bluetooth
BluetoothController.connect()

Frame.connect(0)
Frame.cap_frame()

redContours,redCenterPoint = Frame.processFrame("red","Town Hall",(0,255,0))

listOfResource = Frame.processResource("yellow","Res",(0,0,255))

#for resource in listOfResource
