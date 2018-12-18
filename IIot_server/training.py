from sklearn.externals import joblib 
import pandas as pd
import numpy as np
import collections
df_test = pd.read_csv('./out.csv', header=0)
ap_name = df_test['ap_name'][0]
df_test = df_test[['D_total','D_aggregation','D_block']]
array_test = df_test.values
clf = joblib.load('RVMresult_test19000DF.pkl')
out = clf.predict(array_test)
# print out
out = np.round_(out)
print(collections.Counter(out))

import paho.mqtt.client as mqtt
import time
import prototype

MQTT_SERVER_IP = "140.113.236.57"
MQTT_SERVER_PORT = 1883


client = mqtt.Client("", True, None, mqtt.MQTTv31)
client.connect(MQTT_SERVER_IP, 1883, 60)
c = collections.Counter(out)
_size = max(c, key=c.get)
# if out[0] == 1:
# 	_size = 3
# if out[0] == 3:
# 	_size = 1
device_ap01 = prototype.json_set_aggregator_item(ap_name,factor_size=int(_size))
aggregation_factor_msg = prototype.json_set_aggregator(device_ap01)
client.publish("iiot/factor_size",aggregation_factor_msg)
client.disconnect()

import firebase
firebase.send_FCM("factor","set "+ap_name+" factor size:"+str(_size))
