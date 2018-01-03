import paho.mqtt.client as mqtt
import json
from MongoClient import MongoWrapper
from res import Constant

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("smart_parking/devices")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    data=json.loads(str(msg.payload))
    db.onDeviceData(serial_number=data["serial_number"],status=data["status"])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
db=MongoWrapper.MongoDataBase(host=Constant.host,port=Constant.mongodb_port)

client.connect(Constant.host, Constant.mqttPort, 60)

client.loop_forever()