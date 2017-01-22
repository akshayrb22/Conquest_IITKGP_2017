##Assign to Vasu
##Work on the Blutooth connections
##Functionalities required-
##  connect to bluetooth
##  send commands to slave( ie pi)
##  disconnect
import bluetooth
class BluetoothController(object):
    target_name = "KAIZEN"
    target_address = "B8:27:EB:26:F6:A4"
    nearby_devices = None
    is_connected = False
    port = 1
    sock = None
    #def __init__(se, target_name, target_address,target_port):
    #    target_name = "KAIZEN""
    #    target_address = target_address
    #    port = target_port 

    @staticmethod
    def connect():
        print 'Blutooth Controller Searching for devices... '
        nearby_devices = bluetooth.discover_devices()
        for bluetooth_address in nearby_devices:
            if BluetoothController.target_name == bluetooth.lookup_name(bluetooth_address):
                BluetoothController.is_connected = True
                target_address = bluetooth_address
                if target_address is not None:
                    print "Blutooth Controller  found target with address ", target_address
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
    def send_command(command):
        if BluetoothController.is_connected == True:
            BluetoothController.sock.send(command)
        else:print "Failed to send command... Bluetooth is not connected."
        return
        
if __name__ == '__main__':
    #bluetoothController = BluetoothController("KAIZEN","B8:27:EB:26:F6:A4",1)
    BluetoothController.connect()
    BluetoothController.send_command("s")
    raw_input("Press to close")