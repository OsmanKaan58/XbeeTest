import time
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
from digi.xbee.exception import TimeoutException

# Receiver's XBee address
RECEIVER_ADDRESS = "0013A20040A2828D"

# Initialize the sender XBee device
sender = XBeeDevice("/dev/ttyUSB0", 57600)

def send():
    counter = 11  # Start the counter at 11
    messages_sent = 0  # Counter for messages sent in one second
    start_time = time.time()  # Record the start time

    try:
        sender.open()
        print("Sender is ready to send data.")

        # Create a remote XBee device instance for the receiver
        remote_device = RemoteXBeeDevice(sender, XBee64BitAddress.from_hex_string(RECEIVER_ADDRESS))

        while True:
            # Convert the counter to a string and send it
            message = str(counter) + " Hello from sender\n"
            sender.send_data_async(remote_device, message)
            print(f"Sent data: {message}")

            # Increment the counter for the next message
            counter += 1
            messages_sent += 1

            # Check if one second has passed
            if time.time() - start_time >= 1:
                print(f"Messages sent in the last second: {messages_sent}")
                messages_sent = 0  # Reset the counter
                start_time = time.time()  # Reset the start time

            # Shorter delay to speed up communication
            time.sleep(0.04)

    finally:
        if sender.is_open():
            sender.close()
        print("Sender closed.")

send()