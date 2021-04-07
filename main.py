import GPS_Direction_Logic
from threading import Thread, Lock
import UdpComms as U
import time
import Data_Reader_Library

# Create UDP socket to use for sending (and receiving)

#f = open("GPS_Interface.txt", "r")
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=False)
Datareader = Data_Reader_Library.Datareader(Data_Reader_Library.read_from_UDP, sock)

A = GPS_Direction_Logic.GPS_Direction_Logic(1, Datareader)

while True:
    sentdata = A.plot_course()
    sock.SendData(str(sentdata)) # Send this string to other application

    data = sock.ReadReceivedData() # read data

    if data != None: # if NEW data has been received since last ReadReceivedData function call
        print(data) # print new received data
        tmp = data.split(",")
        tmp2 = []
        for x in range(0,1):
            tmp2.append(float(tmp[x]))
        A.update_position(tmp2)
    time.sleep(1)
