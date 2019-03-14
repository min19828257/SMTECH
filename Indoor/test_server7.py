import serial
import asyncore
import socket
import json
import ast
import threading
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import time
from numpy.linalg import inv
import decimal
from kalman import SingleStateKalmanFilter
import requests
from firebase import firebase
from firebase_admin import auth
import firebase_admin
from firebase_admin import credentials

FirstClient = {}
SecondClient = {}
ThirdClient = {}

Child_location = {}
list_client=[]

Xlist = []
Ylist = []

#GPS start
#gps = serial.Serial("/dev/ttyACM0", baudrate = 9600)

class child_inf:
    def __init__(self):
        self.child_infos = []
        self.ready_child = []

    @staticmethod
    def plus(mac_id,x_value,y_value):
        x_value = str(x_value);y_value=str(y_value);mac_id=str(mac_id)
        Senten = mac_id+","+x_value+","+y_value
        Number.child_info.append(Senten)

    @staticmethod
    def cal():
        if(len(Number.child_info) < 8):
                print("return")
                return
        print(Number.child_info)
        set_li=[]
        for i in range(len(Number.child_info)):
            imac,ix,iy = Number.child_info[i].split(",")
            set_li.append(imac)

        set_li=list(set(list(set_li)))

        for i in range(len(set_li)):
            imac = set_li[i]
            cnt=0
            for j in range(len(Number.child_info)):
                jmac,jx,jy = Number.child_info[j].split(",")
                if(i!=j and imac == jmac):
                    cnt+=1
                    if(cnt > 8):
                        using_li = []
                        for k in range(len(Number.child_info)):
                            kmac,kx,ky = Number.child_info[k].split(",")
                            if(jmac == kmac):
                                using_li.append(kx+","+ky)
#                                print("confirm hochool!!!")
                        result = child_inf.confirm(jmac,using_li)
                        Number.ready_child.append(result)
                        break

#       print("child_inf : ",Number.ready_child)
        if(len(Number.ready_child)>0):
                child_inf.transmit(Number.ready_child)
                Number.ready_child=[]

        print("this is child_inf.ready_child : ",Number.ready_child)

#        Number.child_info = []
    @staticmethod
    def confirm(Mac,lis):
        Upcnt=0;Downcnt=0
        XV=0;YV=0
        for i in range(len(lis)):
            xvalue,yvalue=lis[i].split(",")
            xvalue = float(xvalue);yvalue=float(yvalue)
#            print("====================confirm========================")
#            print("Mac : ",Mac, " xvalue : ",xvalue," yvalue : ",yvalue)
#            print("====================confirm========================")
            if(xvalue > 0 and yvalue<10):
                Upcnt += 1
            else:
                Downcnt += 1
        if(Downcnt>Upcnt):
            status=True
        else:
            status=False

        result = str(Mac)+","+str(status)
        return result
#	print("finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#        child_inf.transmit(Mac,status)

    @staticmethod
    def transmit(lis):

	#SET THE FIREBASE
        print("SET THE FIREBASE")
#        cred = credentials.Certificate("./path/to/serviceAccountKey.json")
#        firebase_admin.initialize_app(cred)
        user = auth.get_user_by_email('kerylaw73@gmail.com')
        print('Successfully fetched user data: {0}'.format(user.uid))

        children_data=OrderedDict()
        #set the busid
        busid = "hellobus"
        children_data["busid"]=busid

       # set the longitude and latitude

       # line = gps.readline()
       # data = line.split(",")
       # if data[0] == "$GPRMC":
       #     if data[2] == "A":
       #         latitude = data[3]
       #         longitude = data[5]
       #         button = 1

        button=0
        if(button != 1):
                latitude="9999"
                longitude="9999"
        l=[0,1];l[0]=latitude;l[1]=longitude
        children_data["l"]=l

        # set the students list
        students = []
        for i in range(len(lis)):
            studic={}
            mac,boool=lis[i].split(",")
            studic["stuid"]=mac
            studic["in"]=boool
            studic["danger"]=False
            students.append(studic)
        children_data["students"]=students

       # busid=cmdline('cat /proc/cpuinfo | grep Serial | awk \'{print$3}\'').strip()

#	array='{"busid":"busid","lat" : '+"\""+latitude+"\""+',"lon":'+"\""+longitude+"\""+',"students" :['
#        array='{"busid":"busid"','"l" : ['+"\""+latitude+"\""+","+"\""+longitude+"]"+",students"+' :['

        result = firebase.put('/driversAvailable', user.uid, children_data )
        
        print("Format : ",json.dumps(children_data, ensure_ascii=False, indent="\t"))
        print("result : ",result)
        #r = requests.post(url,json=payload)

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
#        return kalman_filter_estimates[0],kalman_filter_estimates[1]

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

def Prepare():      #this is for 2
    global data,dict1
    a= '1.112'
    b= '2.223'
    c= " "
    text=a+c+b
    dict1 = {"id1":text,"id2":text}
    data = "hello"
#    line = gps.readline()
    data = line.split(",")
    button=0
    if data[0] == "$GPRMC":
        if data[2] == "A":
            latitude = data[3]
            longitude = data[5]
            button = 1
    if button!=1:
        latitude="9999"
        longitude="7777"
    print("prepare~~~~~~~~~~~~~~~~~~~~",latitude,"longitude ",longitude)
#    x = Messenger(name="send")
#    x.start()

class Messenger(threading.Thread): #for server.py

  def run(self):
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect(('192.168.0.16', 9895))
      line = json.dumps(dict1)
      s.sendall(line.encode())
      resp = s.recv(1024)

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        print("Here",Number.num," ",len(FirstClient)," ",len(SecondClient)," ",len(ThirdClient))
        if Number.num > 2 and len(FirstClient)>1 and len(SecondClient)>1 and len(ThirdClient)>1:
            print("timestamp : ", Number.timestamp)
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
                        x1=6;y1=6;x2=0;y2=6;x3=0;y3=0
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
#			print(d1," ",d2," ",d3)
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
		#	print("MacAddr : ",MacAddr,"X : ",round(Decimal_X,3),"Y : ",round(Decimal_Y,3))
                        original_line = "MacAddr : ",MacAddr,"X : ",round(Decimal_X,3),"Y : ",round(Decimal_Y,3)
                        prepare_server = {}
                        for key, value in il.Mac_dict.items():
                                X,Y = value.split(" ")
                                X,Y = Kalman(float(X),float(Y))
                                if(key == "Client"):
                                       continue
                                print("Kalman MacAddr : ",key,"X : ",round(decimal.Decimal(X),3),"Y : ",round(decimal.Decimal(Y),3))
                                Kalman_line = "Kalman MacAddr : ",key,"X : ",round(decimal.Decimal(X),3),"Y : ",round(decimal.Decimal(Y),3)
                                child_inf.plus(key,round(decimal.Decimal(X),3),round(decimal.Decimal(Y),3))
                                prepare_server[key] = str(X)+" "+str(Y)
                        Child_location.update({MacAddr:X_Y})
                        Child_location.clear()

            print("###########################################################################################")
            il.Mac_dict.clear()
            FirstClient.clear()
            SecondClient.clear()
            ThirdClient.clear()
            Child_location.clear()
        else:
                #prepare for transmit
                flag = False;initial = False

         	# Define timestamp
                Number.timestamp = float(time.time())-float(Number.start_time)

		# Define the data
                prepare_dict_data = {}
                dict_data = {}

                IDlist = []
                Distance =[]
#		print("first")
		#receive data and decode
                data = self.recv(8192)
                prepare_dict_data = json.loads(data.decode('utf-8'))
                dict_data = ast.literal_eval(json.dumps(prepare_dict_data))

                print("dict_data : ", dict_data)
                IDlist = list(dict_data.keys())
                Distance = list(dict_data.values())

                for i in range(len(IDlist)):
                        print("Idlist : ",IDlist[i])

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

		#prepare to transmit to the company server
                if(int(Number.timestamp%10) == 1 or int(Number.timestamp%10) == 5 or int(Number.timestamp%10) == 9):
                        flag = True
		#initialize the time as 0
                if(int(Number.timestamp) > 100):
                        initial = True
                        Number.start_time = time.time()
                        print("Number : ",Number.timestamp)

		#excute the calculate
                if(flag):
                        print("timestamp : ", Number.timestamp)
                        child_inf.cal()
                        print("finish the cal()")
                        #flag = False

                if(initial):
                        Number.child_info = []
                        print("initial : ", Number.child_info)
                        initial=False


                print("receive..")
                data ="ok"
                self.send(data.encode("utf-8"))

    def handle_close(self):
                print("======================Server: Connection Closed========================")
                self.close()

class Number:
    i = 0
    num = 0
    start_time=0
    timestamp = 0
    child_info = []
    ready_child = []

class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        #SET THE FIREBASE
        print("SET THE FIREBASE")
        cred = credentials.Certificate("./path/to/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        #ACCESS TO DB
        print("ACCESS TO BD")
        global firebase
        firebase = firebase.FirebaseApplication("https://kindersafety-83c44.firebaseio.com/", None)
        print("1start1")
 #       Prepare()

    def handle_accept(self):
        Number.start_time = float(time.time())
        Number.num += 1
        print("time : ",Number.start_time)
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print ('Incoming connection from %s' % repr(addr))
            handler = EchoHandler(sock)


server = EchoServer('192.168.35.16', 9011)
asyncore.loop()
