import prototype
###############################################
# set topology of network

global topology
global iptable
global factor_size
topology = {}
iptable = {}
factor_size = {}

wpa2_password = "iiottest"

def set_ip(device_id,ip):
	global iptable
	iptable[device_id] = ip

def get_ip(device_id):
	global iptable
	try:
		return iptable[device_id]
	except KeyError:
		return "0.0.0.0"

def set_factor_size(device_id,size):
	factor_size[device_id] = size

def get_factor_size(device_id):
	global factor_size
	try:
		return factor_size[device_id]
	except KeyError:
		return 0

def generate_factor_json():
	global factor_size
	devices = []
	for (key,value) in factor_size.iteritems():
		devices.append(prototype.json_set_aggregator_item(key,factor_size=value))
	return prototype.json_set_aggregator(*devices)

def add_topology(cluster_head,cluster_member):
	global topology
	if cluster_head not in topology:
		topology[cluster_head] = []
	topology[cluster_head].append(cluster_member)

def add_topology_by_ip(ip,cluster_member):
	cluster_head = get_CH_by_ip(ip)
	add_topology(cluster_head,cluster_member)

def del_topology(cluster_head,cluster_member):
	global topology
	if cluster_head not in topology:
		return False
	try:
		topology[cluster_head].remove(cluster_member)
		return True
	except ValueError:
		return False

def del_topology_by_ip(ip,cluster_member):
	cluster_head = get_CH_by_ip(ip)
	del_topology(cluster_head,cluster_member)

def generate_cluster_json():
	global topology
	devices = []
	for (key,value) in topology.iteritems():
		ip = get_ip(key)
		tmp = prototype.json_set_cluster_item(key,ssid=key,password=wpa2_password,ap_ip=ip,cluster_member=value)
		devices.append(tmp)
	return prototype.json_set_cluster(*devices)

def get_CH_by_CM(cluster_member):
	global topology
	for (key,value) in topology.iteritems():
		if cluster_member in value:
			return key
	return None

def get_CH_by_ip(ip):
	global iptable
	for (key,value) in iptable.iteritems():
		if value == ip:
			return key
	return None

if __name__ == "__main__":
	set_ip("ap01","192.168.31.221")
	add_topology_by_ip("192.168.31.221","sta01")
	del_topology("ap01","sta02")
	add_topology("ap01","sta02")
	del_topology("ap01","sta02")
	set_factor_size("ap01",5)

	print generate_cluster_json()
	print generate_factor_json()
	while True:
		continue