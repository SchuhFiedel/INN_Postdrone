import errno
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import time
import math
from Data_Reader_Library import DataReader
from Data_Writer_Library import DataWriter
from HightController import AltitudeController
import CustomExceptions
from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import socket
from geopy.distance import distance
# Merken, 1ster Wert = Y, 2ter Wert = x für GPS


class GPS_Direction_Logic:

    def __init__(self, connection_string, offset, target_alt ):
        self.current_position = []
        self.target_alt = target_alt
        self.offset = offset
        self.target_position = []
        try:
            self.vehicle = connect(connection_string, heartbeat_timeout=15, wait_ready=True)

        # Bad TCP connection
        except socket.error as e:
            raise e

        # Bad TTY connection
        except OSError as e:
            raise e

        # API Error
        except APIException as e:
            raise e
        # Other error
        except:
            raise RuntimeError("Something Happened")
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")

            time.sleep(10)
        self.current_target = []
        self.load_targets()

        self.__arm_drone()
        self.active = True

    # get the new target from Update_target
    # def update_target(self):
    #     try:
    #         current_position_string = self.target_fp.readline()
    #         print("TargetPos ", current_position_string)
    #         x_local_position, y_local_position = current_position_string.split(",")
    #         print("Targetx", x_local_position, "Targety", y_local_position)
    #         return_value = [float(x_local_position), float(y_local_position)]
    #         self.__Angle_to_target = 0
    #         return return_value
    #     except IOError as e:
    #         print("error")
    #         if e.errno == errno.EACCES:
    #             return "some default data"
    #         raise e

    def load_targets(self):

        target_fp = open("Target.txt", "r")
        target_text = target_fp.read()
        target_text = target_text.splitlines()
        for position in target_text:
            tmp_positions = position.split(",")
            self.target_position.append(tmp_positions)
        print(self.target_position)
        return

    def update_target(self):
        if len(self.target_position) == 0:
            self.active = False
            return
        self.current_target = self.target_position[0]
        self.target_position.pop(0)


    def update_position(self):

        try:
            self.current_position = []
            locationstring = self.vehicle.location.global_relative_frame
            self.current_position.append(locationstring.lat)
            self.current_position.append(locationstring.lon)
            return

        except:
            raise RuntimeError()
        # try:
        #     self.__Current_Position = self.Reader.return_positional_data()
        # except IOError as e:
        #     print("error")
        #     if e.errno == errno.EACCES:
        #         return "some default data"
        #     raise e

    def vector_length(self, vector):
        try:
            sumation = 0
            for number in vector:
                sumation = sumation + number * number

            sumation = np.sqrt(sumation)
            return sumation
        except:
            print("error" + errno)
            raise errno

    # normalize the movement vector
    def vector_normalize(self, vector_len, vector):
        try:
            return_values = []
            for number in vector:
                return_values.append(number / vector_len)
            return return_values
        except:
            print("error" + errno)
            raise errno

    # Calculate Radion of a Vector
    # def calc_rad(self, vector_len, movement_vector):
    #     try:
    #         y_val = movement_vector[0] / vector_len
    #         #print("Y_Val", y_val)
    #         return_value = np.arccos(y_val)
    #         return return_value
    #     except TypeError as e:
    #         print("error", e)
    #         raise
    # convert Radian to degree
    # def rad_to_ang(self, vector_rad, movement_vector):
    #     try:
    #         returnval = np.rad2deg(vector_rad)
    #         if movement_vector[1] < 0:
    #             returnval = abs(returnval - 360)
    #         # Wenn wir mir Einheitskreis rechenn dann muss der Returnval + 90 modulo 360
    #         return returnval
    #     except TypeError as e:
    #         print("error", e)
    #         raise

    # general program object
    active = 1
    GPS_FP = 0



    __Movement = []  # Movementvector to reach target



    def __arm_drone(self):
        print("Arming motors")
        self.vehicle.airspeed = 3
        # Copter should arm in GUIDED mode
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True
        while not self.vehicle.armed:
            print(" Waiting for arming...")

            time.sleep(0.1)

    def reach_operation_height(self):
        while True:
            alt = float(self.vehicle.location.global_relative_frame.alt)
            if alt >= self.target_alt * 0.95:
                print(alt)
                print("Reached target altitude")
                break

        return

    def main_logic(self):
        try:
            self.vehicle.simple_takeoff(self.target_alt)
            self.reach_operation_height()


            while True:
                self.update_target()
                self.update_position()
                #print(self.current_target)
                if not self.active:
                    break
                point = LocationGlobalRelative(float(self.current_target[0]), float(self.current_target[1]),
                                               float(self.target_alt))
                self.vehicle.simple_goto(point)
                while True:
                    time.sleep(1)
                    self.update_position()
                    print(self.current_position)
                    if self.__is_within_offset():
                        break


        except APIException:
            raise APIException
    def __is_within_offset(self):
        coords_1 = (self.current_target[0], self.current_target[1])
        coords_2 = (self.current_position[0], self.current_position[1])

        dist = distance(coords_1, coords_2).km*1000
        print("Distance in meters" + str(dist))

        if dist < self.offset:
            return True
        else:
            return False


        return
    # def display_plot(self):
    #     d = {
    #         "Latitude": [self.__Current_Position[0], self.__TargetPosition[0]],
    #         "Longitude": [self.__Current_Position[1], self.__TargetPosition[1]],
    #     }
    #     df = pd.DataFrame(data=d)
    #
    #     # Plot Graph for easier Display
    #     BBox = (
    #         min(d["Longitude"]) - 0.002,
    #         max(d["Longitude"]) + 0.002,
    #         min(d["Latitude"]) - 0.002,
    #         max(d["Latitude"]) + 0.002,
    #     )
    #     city_map = plt.imread("map.jpg")
    #     fig, ax = plt.subplots(figsize=(8, 7))
    #     # print(df)
    #     ax.scatter(df.Longitude, df.Latitude, s=10, c="red", alpha=1)
    #     ax.set_title("Waypoints Where we need to go")
    #     ax.set_xlim(BBox[0], BBox[1])
    #     ax.set_ylim(BBox[2], BBox[3])
    #     ax.imshow(city_map, zorder=0, extent=BBox)
    #     plt.show()

    def plot_course(self, should_display=False):

        if type(should_display) != bool:
            raise AttributeError
        # print(self.__Current_Position)
        # Calculate the Movement Vector
        try:
            self.__Movement = []
            # Calculate Movement(Velocity) vector
            self.__Movement.append(
                self.__TargetPosition[0] - self.__Current_Position[0]
            )
            self.__Movement.append(
                self.__TargetPosition[1] - self.__Current_Position[1]
            )

        except IOError as e:
            print("Error: ", e)
            raise
        try:
            movement_length = self.vector_length(self.__Movement)
            movement_normalized = self.vector_normalize(
                movement_length, self.__Movement
            )
            # print(movement_normalized)
            self.__Angle_to_target = (
                math.atan2(self.__Movement[1], self.__Movement[0]) * 180 / math.pi
            )
            if self.__Angle_to_target < 0:
                self.__Angle_to_target += 360
        except errno:
            print(errno)
        if should_display:
            self.display_plot()
        # self.active = 0
        if movement_length < self.__Offset:
            self.__Angle_to_target = -1
        # print("Angle: ", self.__Angle_to_target)
        return self.__Angle_to_target
