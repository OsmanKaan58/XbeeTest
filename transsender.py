import serial
import time

# Open serial connection
sender = serial.Serial("/dev/ttyUSB0", 57600)

try:
    counter = 0
    while True:
        message = f"{counter} Hello from sender"
        sender.write(message.encode("utf-8"))  # Send data
        print(f"Sent: {message}")
        counter += 1
        time.sleep(0.1)  # Adjust delay as needed

finally:
    sender.close()
