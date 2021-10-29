import GPS_Direction_Logic
import UdpComms as U
import Data_Reader_Library
import Data_Writer_Library
import HightController
from dronekit import connect
from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time


A = GPS_Direction_Logic.GPS_Direction_Logic('tcp:127.0.0.1:5760', offset=0.5, target_alt=40)
A.main_logic()

