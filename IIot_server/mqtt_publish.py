import paho.mqtt.client as mqtt

import prototype

global client
client = None

MQTT_SERVER_IP = "140.113.179.7"
MQTT_SERVER_PORT = 1883