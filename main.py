import GPS_Navigator

import UdpComms as U
import time

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

A = GPS_Navigator.GPS_Direction_Logic()

while True:
    sentdata = A.plot_course()
    sock.SendData(str(sentdata)) # Send this string to other application

    data = sock.ReadReceivedData() # read data

    if data != None: # if NEW data has been received since last ReadReceivedData function call
        print(data) # print new received data
        GPS_FP = open("GPS_Interface.txt", "w")
        GPS_FP.write(data)
    time.sleep(1)
