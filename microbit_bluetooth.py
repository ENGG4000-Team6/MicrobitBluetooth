# Write your code here :-)
from microbit import *
import ubluetooth

# Service name to be broadcasted
PERIPHERAL_NAME = "BioSync Dummy Device"
SERVICE_UUID = ubluetooth.UUID("CD9CFC21-0ECC-42E5-BF22-48AA715CA112")
CHARACTERISTIC_INPUT_UUID = ubluetooth.UUID("66E5FFCE-AA96-4DC9-90C3-C62BBCCD29AC")
CHARACTERISTIC_OUTPUT_UUID = ubluetooth.UUID("142F29DD-B1F0-4FA8-8E55-5A2D5F3E2471")

# Output characteristic is used to send the response back to the connected phone
pOutputChar = None

# Class defines methods called when a device connects and disconnects from the service
class ServerCallbacks:
    def __init__(self):
        pass

    def on_connect(self, pServer):
        print("BLE Client Connected")

    def on_disconnect(self, pServer):
        ubluetooth.start_advertising(adv)

class InputReceivedCallbacks:
    def __init__(self):
        pass

    def on_write(self, pCharWriteState):
        inputValue = pCharWriteState.value()
        if inputValue:
            print("Received Value: " + inputValue.decode())
            # Send data to client
            outputData = "Last received: " + inputValue.decode()
            pOutputChar.value(outputData)
            pOutputChar.notify()

# Initialize Bluetooth
ble = ubluetooth.BLE()

# Create the server
pServer = ble.gatts

# Create the service
pService = pServer.add_service(SERVICE_UUID)

# Handle inputs (sent from app)
pInputChar = pService.add_characteristic(
    CHARACTERISTIC_INPUT_UUID,
    properties=ubluetooth.CHAR_WRITE | ubluetooth.CHAR_WRITE_NR
)

pOutputChar = pService.add_characteristic(
    CHARACTERISTIC_OUTPUT_UUID,
    properties=ubluetooth.CHAR_READ | ubluetooth.CHAR_NOTIFY
)

# Set server callbacks
pServer.callbacks(ServerCallbacks())

# Set input callbacks
pInputChar.callbacks(InputReceivedCallbacks())

# Start advertising
adv = ubluetooth.ADVERTISING_DATA_NAME_COMPLETE
ble.active(True)
ble.config(adv_data=adv)

while True:
    pass
