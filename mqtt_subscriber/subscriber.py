import paho.mqtt.client as mqtt
import json
import serial
import time
from datetime import datetime

# Serial connection to Arduino
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)  # Wait for connection to establish
    print("Connected to Arduino")
except Exception as e:
    print(f"Failed to connect to Arduino: {e}")
    ser = None

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe("light/schedule")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        on_time = data.get('onTime')
        off_time = data.get('offTime')
        
        print(f"Received schedule - ON: {on_time}, OFF: {off_time}")
        
        # Here you would implement the logic to compare current time
        # with scheduled times and send commands to Arduino
        # For now, just print the received schedule
        
    except Exception as e:
        print(f"Error processing message: {e}")

def check_schedule():
    # This function would be called periodically to check if current time
    # matches any scheduled times and send commands to Arduino
    # For a complete implementation, you would need to store the schedule
    # and compare with current time
    pass

# Set up MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect("localhost", 1883, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("Disconnecting...")
    client.disconnect()
    if ser:
        ser.close()