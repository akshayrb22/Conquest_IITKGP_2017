##Assign to Vasu
##Work on the Blutooth connections
##Functionalities required-
##  connect to bluetooth
##  send commands to slave( ie pi)
##  disconnect

from multiprocessing import Process
import bluetooth
from time import sleep
from FindDirectionality import Orientation,MovementFunctions,Direction
class BluetoothController(object):
    target_name = "HC-06"
    target_address = "B8:27:EB:26:F6:A4"
    nearby_devices = None
    is_connected = False
    port = 1
    sock = None
    prevCommand = ""
    command = "s"
    #def __init__(se, target_name, target_address,target_port):
    #    target_name = "KAIZEN""
    #    target_address = target_address
    #    port = target_port 

    @staticmethod
    def connect():
        print 'Bluetooth Controller Searching for devices... '
        nearby_devices = bluetooth.discover_devices()
        for bluetooth_address in nearby_devices:
            if BluetoothController.target_name == bluetooth.lookup_name(bluetooth_address):
                BluetoothController.is_connected = True
                BluetoothController.target_address = bluetooth_address
                if BluetoothController.target_address is not None:
                    print "Bluetooth Controller  found target with address ", BluetoothController.target_address
                    BluetoothController.connect_to_slave()
                                      
                else:
                    print "could not find target bluetooth device nearby"                  
                break
    @staticmethod
    def connect_to_slave():
        BluetoothController.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print "Bluetooth Controller  >> Connecting to Slave...."
        BluetoothController.sock.connect((BluetoothController.target_address, BluetoothController.port))
        print"Bluetooth Controller conected success"
    @staticmethod    
    def disconnect():
        BluetoothController.sock.close()
    @staticmethod
    def send_command(command,message = None):

        #send all command
        #print message
        if command != BluetoothController.prevCommand:
            if message == None:
                print "Sent command " + command
            else:
                print message
        if BluetoothController.is_connected == True:
            BluetoothController.sock.send(command)
            BluetoothController.prevCommand = command
        
        #     if BluetoothController.is_connected == True:
        #         BluetoothController.prevCommand = command
        #         BluetoothController.sock.send(command)
        return 

def parallelProcess(command):
    BluetoothController.connect()
    while True:
        print "sending  command " + command
        BluetoothController.send_command(command)
        sleep(1)

if __name__ == '__main__':
    #bluetoothController = BluetoothController("KAIZEN","B8:27:EB:26:F6:A4",1)
    command = "s"
    #bluetoothProcess = Process(target=parallelProcess,args=(command))
    #bluetoothProcess.start()
    #bluetoothProcess.join()
    BluetoothController.connect()
    while True:
        command = raw_input("Enter command: ")
        print " >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + command
        #BluetoothController.command = command
        BluetoothController.send_command(command)
        