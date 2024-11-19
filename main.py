import time
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
from digi.xbee.exception import TimeoutException


# Receiver's XBee address
RECEIVER_ADDRESS = "0013A20040A2828D"

# Initialize the sender XBee device
sender = XBeeDevice("/dev/ttyUSB0", 230400)

def send():
    counter = 11  # Start the counter at 1000001
    try:
        sender.open()
        print("Sender is ready to send data.")

        # Create a remote XBee device instance for the receiver
        remote_device = RemoteXBeeDevice(sender, XBee64BitAddress.from_hex_string(RECEIVER_ADDRESS))

        while True:
            # Convert the counter to a string and send it
            message = str(counter) + " Hello from sender\n"
            message2 = "6,2,1530065,1550025,0,0,0,0,0,0"
            sender.send_data_async(remote_device, message2)
            print(f"Sent data: {message2}")

            # Wait for acknowledgment with a shorter timeout

            # Increment the counter for the next message
            counter += 1

            # Shorter delay to speed up communication
            time.sleep(0.04)

    finally:
        if sender.is_open():
            sender.close()
        print("Sender closed.")

send()

