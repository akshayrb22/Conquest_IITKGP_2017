##Assign to Vasu
##Work on the Blutooth connections
##Functionalities required-
##  connect to bluetooth
##  send commands to slave( ie pi)
##  disconnect
import bluetooth
class BlutoothController(object):
    def __init__(self, target_name, py_address):
        self.target_name = "KAIZEN"
        self.target_address = None
        self.nearby_devices = None
        self.is_connected = False
        self.py_address = "B8:27:EB:26:F6:A4"
        self.port = 1
        self.sock = None

    def connect(self):
        self.nearby_devices = bluetooth.discover_devices()
        for bluetooth_address in self.nearby_devices:
            if self.target_name == bluetooth.lookup_name(bluetooth_address):
                self.is_connected = True
                self.target_address = bluetooth_address
                if self.target_address is not None:
                    print "found target bluetooth device with address ", self.target_address
                else:
                    print "could not find target bluetooth device nearby"
                break
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print "Connecting to Slave...."
        self.sock.connect((self.py_address, self.port))

    def bluetooth_disconnect(self):
        self.sock.close()

    def send_command(self,command):
        self.sock.send(command)
        