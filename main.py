import GPS_Direction_Logic
import UdpComms as U
import Data_Reader_Library
import Data_Writer_Library
import HightController
# Create UDP socket to use for sending (and receiving)

f = open("GPS_Interface.txt", "r")
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=False)
Datareader = Data_Reader_Library.DataReader(Data_Reader_Library.read_from_udp, sock)
Datawriter = Data_Writer_Library.DataWriter(Data_Writer_Library.send_to_UDP, sock)
Hightcontroller = HightController.HeightController(3)
A = GPS_Direction_Logic.GPS_Direction_Logic(0, Datareader, Datawriter, Hightcontroller)
A.thread_wrapper()
print(A.plot_course())
# while True:
#     sentdata = A.plot_course()
#     sock.SendData(str(sentdata)) # Send this string to other application
#
#     data = sock.ReadReceivedData() # read data
#
#     if data != None: # if NEW data has been received since last ReadReceivedData function call
#         print(data) # print new received data
#         tmp = data.split(",")
#         tmp2 = []
#         for x in range(0,1):
#             tmp2.append(float(tmp[x]))
#         A.update_position(tmp2)
#     time.sleep(1)
