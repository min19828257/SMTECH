import asyncore
import socket
import json
import ast
import threading
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from numpy.linalg import inv
import decimal
from kalman import SingleStateKalmanFilter

FirstClient = {}
SecondClient = {}
ThirdClient = {}

Child_location = {}
list_client=[]

Xlist = []
Ylist = []

#Write something
def WriteTxt1(st):
        file = open('ouput1.txt', 'a')
        line = str(st)
        file.write(line)
        file.write('\n')
def WriteTxt2(st):
        file = open('ouput2.txt', 'a')
        line = str(st)
        file.write(line)
        file.write('\n')

#Make the Kalman
def Kalman(NX,NY):
	# Create some random temperature data
	random_data = (NX,NY)

	# Initialise the Kalman Filter

	A = 1  # No process innovation
	C = 1  # Measurement
	B = 0  # No control input
	Q = 0.005  # Process covariance
	R = 1  # Measurement covariance
	x = 0  # Initial estimate
	P = 1  # Initial covariance

	kalman_filter = SingleStateKalmanFilter(A, B, C, x, P, Q, R)

	# Empty lists for capturing filter estimates
	kalman_filter_estimates = []

	# Simulate the data arriving sequentially
	for data in random_data:
	    kalman_filter.step(0, data)
	    kalman_filter_estimates.append(kalman_filter.current_state())
#	print("kalman values: ", kalman_filter_estimates[0]," : ", kalman_filter_estimates[1])
        return kalman_filter_estimates[0],kalman_filter_estimates[1]

class ilist:
	item = []
	Mac_dict = {}

	def initialize(self):
		Mac_dict.clear()
		Mac_dict = {}

	def initial(self, inilist):
		self.Mac_dict = {}
		for i in inilist:
			result = str(0)+" "+str(0)
			self.Mac_dict[i]=result

	def append(self,Mac,X,Y):
		for i in self.item:
			if Mac == i:
				result = str(X)+" "+str(Y)
				self.Mac_dict[Mac]=result

	def input(self,ilist):
		for i in ilist:
			self.item.append(i)
		self.item = list(set(self.item))

def draw(a,b):
    x=float(a)
    y=float(b)

    plt.cla()
    plt.grid(True)
    plt.xlabel("X data")
    plt.ylabel("Y data")
    plt.title("Title")
    plt.scatter(float(x),float(y))
    plt.xlim(0,3)
    plt.ylim(0,3)
#    plt.scatter(10,10)
#    plt.scatter(10,0)
#    plt.scatter(0,10)

    fig = plt.gcf()
    fig.savefig("GG.png")

def Prepare():      #this is for 2

    global data,dict1
    a= '1.112'
    b= '2.223'
    c= " "
    text=a+c+b
    dict1 = {"id1":text,"id2":text}
    data = "hello"
    x = Messenger(name="send")
    x.start()

class Messenger(threading.Thread): #for server.py

  def run(self):
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect(('192.168.0.16', 9895))
      line = json.dumps(dict1)
      s.sendall(line.encode())
      resp = s.recv(1024)

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
#	print("Here")
        if Number.num > 2 and len(FirstClient) >2 and len(SecondClient)>2 and len(ThirdClient)>2:
            #################Calculate X,Y#########################
	    Firstlocation = [1,1]
	    Secondlocation = [2,2]
	    Thirdlocation = [1,3]

            #extract data that is items and combine and make the condition
            items_list = []

            for key,value in FirstClient.items():
                        items_list.append(key)
            for key,value in SecondClient.items():
                        items_list.append(key)
            for key,value in ThirdClient.items():
                        items_list.append(key)

            items_list = list(set(items_list))

            #make the ilist
            il = ilist()
            il.input(items_list)
            print("###########################################################################################")

            inilist = []
            for key in items_list:
#			inilist.append(key)
			X_Y = []
			MacAddr = key
			global d1, d2, d3
			x1=2.2;y1=0;x2=2.2;y2=1.5;x3=0;y3=0
			print("Start------------")
			for fkey, fvalue in FirstClient.items():
					if MacAddr == fkey:
						distance1 = fvalue
						d1 = float(distance1)

			for skey, svalue in SecondClient.items():
                                        if MacAddr == skey:
                                                distance2 = svalue
						d2 = float(distance2)
			for tkey, tvalue in ThirdClient.items():
                                        if MacAddr == tkey:
                                                distance3 = tvalue
						d3 = float(distance3)
			print(d1," ",d2," ",d3)
			#Calculate X_Y
			C = d1**2-d2**2-x1**2+x2**2-y1**2+y2**2
                        E = -2*y2+2*y3
                        F = d2**2-d3**2-x2**2+x3**2-y2**2+y3**2
                        B = -2*y1+2*y2
                        A = -2*x1+2*x2
                        D = -2*x2+2*x3

			X = (C*E-F*B)/(E*A-B*D)
			Y = (C*D-A*F)/(B*D-A*E)
			X_Y.append(X)
			X_Y.append(Y)
			Decimal_X = decimal.Decimal(X)
			Decimal_Y = decimal.Decimal(Y)
			il.append(MacAddr,round(Decimal_X,3),round(Decimal_Y,3))
			print("MacAddr : ",MacAddr,"X : ",round(Decimal_X,3),"Y : ",round(Decimal_Y,3))
			original_line = "MacAddr : ",MacAddr,"X : ",round(Decimal_X,3),"Y : ",round(Decimal_Y,3)
			if(MacAddr!="Client" or MacAddr =="c2:01:18:00:00:cd" or MacAddr=="c2:01:18:00:00:b3" or MacAddr=="c2:01:18:00:00:da"):
				WriteTxt1(original_line)
			prepare_server = {}
                        for key, value in il.Mac_dict.items():
				X,Y = value.split(" ")
				X,Y = Kalman(float(X),float(Y))
				if(key == "Client"):
					continue
				print("Kalman MacAddr : ",key,"X : ",round(decimal.Decimal(X),3),"Y : ",round(decimal.Decimal(Y),3))
 				Kalman_line = "Kalman MacAddr : ",key,"X : ",round(decimal.Decimal(X),3),"Y : ",round(decimal.Decimal(Y),3)
				if(MacAddr =="c2:01:18:00:00:cd" or MacAddr=="c2:01:18:00:00:b3" or MacAddr=="c2:01:18:00:00:da"):
					WriteTxt2(Kalman_line)
				prepare_server[key] = str(X)+" "+str(Y)
			WriteTxt2('\n')
                        Child_location.update({MacAddr:X_Y})
			Child_location.clear()

	    print("###########################################################################################")
            il.Mac_dict.clear()
            FirstClient.clear()
	    SecondClient.clear()
	    ThirdClient.clear()
	    Child_location.clear()

        else:
		# Define the data
                prepare_dict_data = {}
                dict_data = {}

        	IDlist = []
        	Distance =[]
#		print("first")
		#receive data and decode
        	data = self.recv(8192)
        	prepare_dict_data = json.loads(data)
        	dict_data = ast.literal_eval(json.dumps(prepare_dict_data))

        	IDlist = dict_data.keys()
        	Distance = dict_data.values()

		#Classify Beacon and update ID,Distance
		for value in Distance:
			if value == 1:
				for i in range(0,len(IDlist)):
					FirstClient.update({IDlist[i]:Distance[i]})
			elif value == 2:
				for i in range(0,len(IDlist)):
                                        SecondClient.update({IDlist[i]:Distance[i]})
                        elif value == 3:
                                for i in range(0,len(IDlist)):
                                        ThirdClient.update({IDlist[i]:Distance[i]})

		print("receive..")

    def handle_close(self):
		print("======================Server: Connection Closed========================")
		self.close()

class Number:
    i = 0
    num = 0

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
	Number.num += 1
        if pair is not None:
            sock, addr = pair
            print ('Incoming connection from %s' % repr(addr))
            handler = EchoHandler(sock)


server = EchoServer('192.168.0.16', 9011)
asyncore.loop()
