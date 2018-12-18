from __future__ import division
import matplotlib.pyplot as plt

import csv

import pandas as pd
import numpy as np
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def ecludiean_distance(x,y):
	return np.linalg.norm(x-y)

df_logcols=['STA_ID', \
            'STA_generate_time', \
            'delay', \
            'server_catch_time']

file_name = "server_file.csv"

df_logfile = pd.read_csv(file_name, header=0, names=df_logcols)

print(len(df_logfile.groupby(['STA_ID']).groups.keys()))

station_size =int(len(df_logfile.groupby(['STA_ID']).groups.keys()))
print df_logfile.groupby(['STA_ID']).groups.keys()

partition =2

box = [ [] for i in range(partition)]

files=[file_name]
for file in files:

	mean_value = {}
	quantity = {}
	std_value = {}
	collect_delay_modify = {}
	collect_time_modify = {}
	for i in range(1,station_size+1):
		print i
		tmp = ( "0" + str(i) ) if ( i < 10 ) else str(i)
		mean_value['sta'+tmp] = 0
		quantity['sta'+tmp] = 0
	print mean_value
	counter = 1
	collect_delay, collect_time = {},{}
	for i in range(1,station_size+1):
		tmp = ( "0" + str(i) ) if ( i < 10 ) else str(i)
		collect_delay["sta"+tmp] = []
		collect_time['sta'+tmp] = []
	with open(file,'r') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if(len(row) == 4):
				collect_delay[row[0]].append(float(row[2]))
				collect_time[row[0]].append(row[3])
				counter+=1
			#print collect_delay[row[0]]
		print counter

	up_bound = {}
	low_bound = {}

	for i in range(1,station_size+1):
		tmp = ( "0" + str(i) ) if ( i < 10 ) else str(i)
		quantity['sta'+tmp]= len(collect_delay['sta'+ tmp])
		up_bound["sta"+tmp] = ( mean(collect_delay['sta'+ tmp]) + np.std(collect_delay['sta'+ tmp])*2)
		low_bound['sta'+ tmp] = ( mean(collect_delay['sta'+ tmp]) - np.std(collect_delay['sta'+ tmp])*2)
	
	keys = []
	for i in range(1,station_size+1):
		tmp = ( "0" + str(i) ) if ( i < 10 ) else str(i)
		keys.append( "sta"+tmp )
		collect_delay_modify["sta"+tmp] = []
		collect_time_modify["sta"+tmp] = []

	for key in keys:
	    for item in collect_delay[key]:
			if (item < up_bound[key] and item < 5000) and (item > low_bound[key] and item > 0) :
				index = collect_delay[key].index(item)
				collect_delay_modify[key].append(item)
				collect_time_modify[key].append(collect_time[key][index])

	for i in range(1,station_size+1):
		tmp = ( "0" + str(i) ) if ( i < 10 ) else str(i)
		mean_value['sta'+ tmp] = mean(collect_delay_modify['sta'+ tmp])
	
	from sklearn.preprocessing import normalize
	quantity = list(quantity.values())
	mean_value = list(mean_value.values())
	print(mean(mean_value))
	quantity = quantity / np.linalg.norm(quantity)
	mean_value = mean_value / np.linalg.norm(mean_value)

	bins = {}
	total_item = 0
	for i in range(len(quantity)):
		value = 0.3*quantity[i]+0.7*mean_value[i] 
		bins[str(i)] = value
		total_item += value

	partition = 2
	max_box_size  = total_item/partition

	import operator
	sorted_x = sorted(bins.items(), key=operator.itemgetter(1))
	print sorted_x

	contain = 0
	now_box = 0	
	for key, value in sorted_x:
		if contain <max_box_size:
			contain += value
			box[now_box].append(key)
		else:
			contain = 0
			now_box += 1
			box[now_box].append(key)
	print box

import paho.mqtt.client as mqtt
import time
import prototype
global client
client = None

MQTT_SERVER_IP = "140.113.236.57"
MQTT_SERVER_PORT = 1883

AP_IP = ["192.168.8.100","192.168.8.100"]
AP_ID = ["ap01","ap02"]
client = mqtt.Client("", True, None, mqtt.MQTTv31)
client.connect(MQTT_SERVER_IP, 1883, 60)
counter = 0
for items in box:
	device_member = []
	for i in items:
		tmp = ( "0" + str(int(i)+1) ) if ( int(i)+1 < 10 ) else str(int(i)+1)
		device_member.append('sta'+tmp)
	if len(device_member) == 0:
		continue

	print device_member
	device_1 = prototype.json_set_cluster_item('default',ssid=AP_ID[counter],password='iiottest', \
                                           ap_ip=AP_IP[counter],cluster_member=device_member)
	cluster_msg = prototype.json_set_cluster(device_1)
	print cluster_msg
	counter += 1
	client.publish("iiot/cluster",cluster_msg)
import time
time.sleep(1)
client.disconnect()