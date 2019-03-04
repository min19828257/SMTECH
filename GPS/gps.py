import serial
import os
import requests
import json
from subprocess import PIPE, Popen

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def transmit(busid,latitude,longitude):
	print("busid : ",busid,"latitude : ",latitude,"longitude : ",longitude)
	url=""
	payload={"busid" : busid, "lat":latitude,"lon":longitude}
	r = requests.post(url,json=payload)

gps = serial.Serial("/dev/ttyACM0", baudrate = 9600)

while True:
    print(os.system("ls"))
#    print(os.system("cd /dev && screen ttyACM0 9600"))
    line = gps.readline()
    data = line.split(",")
    busid =cmdline('cat /proc/cpuinfo | grep Serial | awk \'{print$3}\'').strip()
    print(data)
    if data[0] == "$GPRMC":
        if data[2] == "A":
            print("Latitude : ", data[3])
            print("Longitude : ", data[5])
           # transmit(busid,data[3],data[5])
	elif data[2] == "V":
            print("Invalid")
            print(data)
           # transmit(busid,"1","2")
