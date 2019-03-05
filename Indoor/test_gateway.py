#!/usr/bin/python
#*-* coding: utf-8 *-*
from socket import *
import blescan
import sys
import json
import asyncore
import os
import time
from time import sleep
import bluetooth._bluetooth as bluez
from kalman import SingleStateKalmanFilter

list_ID = []
list_RSSI = []

dict_data = {}
dev_id = 0

#Make the Kalman
def Kalman(rssi):
        # Create some random temperature data
        random_data = rssi

        # Initialise the Kalman Filter

        A = 1  # No process innovation
        C = 1  # Measurement
        B = 0  # No control input
        Q = 0.05  # Process covariance
        R = 1  # Measurement covariance
        x = -59  # Initial estimate
        P = 1  # Initial covariance

        kalman_filter = SingleStateKalmanFilter(A, B, C, x, P, Q, R)

        # Empty lists for capturing filter estimates
        kalman_filter_estimates = []

        # Simulate the data arriving sequentially
        for data in random_data:
            kalman_filter.step(0, data)
            kalman_filter_estimates.append(kalman_filter.current_state())
        return kalman_filter_estimates

try:
        sock = bluez.hci_open_dev(dev_id)
        print "ble thread started"

except:
        print "error accessing bluetooth device..."
        sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

HOST='192.168.1.5'

c = socket(AF_INET, SOCK_STREAM)
print 'connecting....'
c.connect((HOST,9011))
print 'ok'
while True:
	list_ID = []
	list_RSSI = []

	dict_data = {}
        returnedList = blescan.parse_events(sock, 10)
        for beacon in returnedList:
                columm_storage = []
                columm_storage = beacon.split(',')
                list_ID.append(columm_storage[0])
#                list_RSSI.append(10**((-59-float(columm_storage[5]))/20))
		list_RSSI.append(float(columm_storage[5]))
		print("MAC : ",columm_storage[0], "RSSI : ",10**((-59-float(columm_storage[5]))/20))
	
	list_RSSI = Kalman(list_RSSI)

	for i in range(0,len(list_RSSI)):
		list_RSSI[i] = 10**((-59-float(list_RSSI[i]))/20)

# Input Client ID
	list_ID.append("Client")
	list_RSSI.append(1)

        for i in range(0,len(list_ID)):
                dict_data.update({list_ID[i]:list_RSSI[i]})
 #       print("finish this update")

        for i in dict_data:
		print(i,"Kalman : " ,dict_data[i])
	print("\n")
        data = json.dumps(dict_data)
        if data:
                c.sendall(data.encode())
        else:
                continue
#        print ('recive_data : ',c.recv(1024))
c.close()

