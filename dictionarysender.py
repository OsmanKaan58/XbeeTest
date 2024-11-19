import time
import json
import ast
from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress

# Receiver's XBee address
RECEIVER_ADDRESS = "0013A20040A2828D"
FILE_PATH = "simulatedData.txt"  # Path to your file containing dictionaries

# Initialize the sender XBee device
sender = XBeeDevice("/dev/ttyUSB0", 230400)


def create_string_from_dictionary(data_dict):
    # Extract the channel value
    channel = data_dict['Channel']

    sensor_num = data_dict['Sensors']

    # Set the maximum number of sensors
    max_sensor_number = 8  # Set this to the maximum expected sensor number

    # Extract all sensor values, including zeros
    sensors = [
        data_dict.get(f'Sensor {i}', 0) for i in range(1, max_sensor_number + 1)
    ]

    # Combine the channel and sensor values into a single list
    values = [channel] + [sensor_num] + sensors

    # Convert the values to a comma-separated string
    return ','.join(map(str, values))


def send():
    try:
        sender.open()
        print("Sender is ready to send data.")

        # Create a remote XBee device instance for the receiver
        remote_device = RemoteXBeeDevice(sender, XBee64BitAddress.from_hex_string(RECEIVER_ADDRESS))

        message_count = 0
        start_time = time.time()

        # Open the file and read each dictionary as a separate line
        with open(FILE_PATH, 'r') as file:
            for line in file:
                # Send each dictionary in the file as a string message

                message = line # Strip any extra whitespace or newline characters
                message = ast.literal_eval(message)
                message = create_string_from_dictionary(message)
                sender.send_data_async(remote_device, message)
                message_count += 1
                print(f"Sent data: {message}")

                if time.time() - start_time >= 1:
                    print(f"Messages sent in the last second: {message_count}")
                    message_count = 0
                    start_time = time.time()
                # Shorter delay to speed up communication
                time.sleep(0.08)

    finally:
        if sender.is_open():
            sender.close()
        print("Sender closed.")

send()