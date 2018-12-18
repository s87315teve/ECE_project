'''
Created on 2013-9-24
Implementint asynchronous I/O using select().The program starts out by creating a nonblocking
TCP/IP socket and configuring it to listen on an address
@author: mupeng
'''
import select
import socket
import Queue
import time
import topology
import thread
import os.path
import mqtt_publish
import numpy as np


#####################################################
# init by server, but it need to be init by mqtt future

#topology.set_factor_size("ap02",1)
#topology.add_topology("ap02","sta07")

#message = topology.generate_factor_json()
#thread.start_new_thread( mqtt_publish.publish ,("iiot/factor_size",message,))
#flag_alert = {}

#####################################################

current_milli_time = lambda: int(round(time.time() * 100000))

import ntplib
client = ntplib.NTPClient()
global offset
offset = 0

def sys_time():	
	while 1:
		while 1:
			try:		
				response = client.request('140.113.236.57')
				ts = int(response.tx_time*100000)
				global offset
				offset = current_milli_time()-ts
				break
			except ntplib.NTPException:
				print "retry ntp"
				time.sleep(1)
		time.sleep(30)

try:
	response = client.request('140.113.236.57')
	ts = int(response.tx_time*100000)
	offset = current_milli_time()-ts
except ntplib.NTPException:
	print "sync fail"

print offset
thread.start_new_thread( sys_time ,())

#create a socket
iiot_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
iiot_server.setblocking(False)
#set option reused
iiot_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR  , 1)
 
iiot_server_address= ("140.113.236.57",7777)
iiot_server.bind(iiot_server_address)
 
iiot_server.listen(10)
 
# sockets from which we except to read
inputs = [iiot_server]

# no output
outputs = []

# A optional parameter for select is TIMEOUT
timeout = 0

tmp_queues = {}

import sys
PATH = './log.csv'
file = open(PATH,'w')

#delay buffer
global buffer_delay
buffer_delay = np.array([])

# send log to mobile phone.
def send_log():
	log_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	log_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR  , 1)
	 
	log_server_address= ("140.113.236.57",8888)
	log_server.bind(log_server_address)
	log_server.listen(1)

	while True:
		# Wait for a connection	  
		try:  
			connection, client_address = log_server.accept()
			connection.sendall(str(np.mean(buffer_delay)))
		finally:
			connection.close()

thread.start_new_thread( send_log ,())

# add the delay data to log server for transmission.
def add_buffer_delay(delay):
	global buffer_delay
	if buffer_delay.size < 5:
		buffer_delay = np.append(buffer_delay, float(delay)/100)
	else:
	 	buffer_delay = np.delete(buffer_delay, 0, 0)
	 	buffer_delay = np.append(buffer_delay, float(delay)/100)



def isDigit(x):
	try:
		float(x)
		return True
	except ValueError:
		return False

def is_write():
	try:
		_flag = open("is_write.txt", "r")
		tmp = int(_flag.read())
		_flag.close()
		return tmp
	except IOError:
		return 0


while inputs:
	print "waiting for next Client"
	print inputs
	readable , writable , exceptional = select.select(inputs, outputs, inputs)
 
	# When timeout reached , select return three empty lists
	if not (readable or writable or exceptional) :
		print "Time out ! "
		break;	
	for s in readable :
		if s is iiot_server:
			# A "readable" socket is ready to accept a connection
			connection, client_address = s.accept()
			print "	connection from ", client_address
			connection.setblocking(0)
			inputs.append(connection)
			tmp_queues[connection] = ""	
		else:	
			try:
				tmp_queues[s] += s.recv(1024)
				if tmp_queues[s] :
					print " received " , tmp_queues[s] , "from ", s.getpeername()
					lines = tmp_queues[s].split('\n')
					flag = 0
					if not tmp_queues[s].endswith('\n'):
						tmp_queues[s] = lines[len(lines)-1]
					else:
						print "almost clear !\n"
						tmp_queues[s] = ""

					del lines[len(lines)-1]

					for line in lines:
						print "message put =>" + line

						msg = line.split(',')
						now_time = current_milli_time()

						# read the delay here!!! 
						delay = now_time - long(msg[1]) - offset
						thread.start_new_thread( add_buffer_delay ,(delay,))
						print "device :" + str(msg[0])
						print "delay : " + str(float(delay)/100)
						print "now_time : " + str(now_time)
						if is_write() == 1:
							if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
								print "writable : " + str(is_write())
								file.write(str(msg[0]) +","+ str(msg[1]) + "," + str(float(delay)/100) + "," + str(now_time- offset) + "\n")
								#file.close()
							else:
								file = open(PATH,'w')						
								file.write(str(msg[0]) +","+ str(msg[1]) + "," + str(float(delay)/100) + "," + str(now_time- offset) + "\n")
								#file.close()
						
						# set alert message
						try:
							
							if isDigit(msg[2]) == False:
								continue
							print "temperture :" + str((float(msg[2])-25)*10+float(msg[2]))
							temperture = (float(msg[2])-25)*10+float(msg[2])						
							
						except IndexError:
							continue
						
	
				else:
					# Interpret empty result as closed connection
					print "closing", s.getpeername()
					inputs.remove(s)
					del tmp_queues[s]
					s.close()
			except:
				inputs.remove(s)
				del tmp_queues[s]
				s.close()
				continue
	for s in exceptional:
		print " exception condition on ", s.getpeername()
		# stop listening for input on the connection
		inputs.remove(s)
		s.close()
		# Remove message queue
		del message_queues

