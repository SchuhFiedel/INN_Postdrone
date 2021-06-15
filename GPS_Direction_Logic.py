import errno
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import time
import math
from Data_Reader_Library import DataReader
from Data_Writer_Library import DataWriter
from HightController import HeightController

# Merken, 1ster Wert = Y, 2ter Wert = x für GPS


class GPS_Direction_Logic:
    def __init__(self, offset: float, dr: DataReader, dw: DataWriter, hc: HeightController):
        self.Reader = dr
        self.Writer = dw

        self.__Target_position = self.update_target()
        self.__Offset = offset
        self.Reader.read_positional_data()
        self.Writer.send_positional_data()
        self.Active = True
        time.sleep(1)

    #get the new target from Update_target
    def update_target(self):
        try:
            target_fp = open("Target.txt", "r")
            current_position_string = target_fp.read()
            x_local_position, y_local_position = current_position_string.split(',')
            return_value = [float(x_local_position), float(y_local_position)]
            return return_value
        except IOError as e:
            print("error")
            if e.errno == errno.EACCES:
                return "some default data"
            raise e

    def update_position(self):
        try:
            self.__Current_Position = self.Reader.return_positional_data()
        except IOError as e:
            print("error")
            if e.errno == errno.EACCES:
                return "some default data"
            raise e

    def vector_length(self, vector):
        try:
            sumation = 0
            for number in vector:
                sumation = sumation + number * number

            sumation = np.sqrt(sumation)
            return sumation
        except:
            print("error")
            raise

    #normalize the movement vector
    def vector_normalize(self, vector_len, vector):
        try:
            return_values = []
            for number in vector:
                return_values.append(number / vector_len)
            return return_values
        except:
            print("error")
            raise

    #Calculate Radion of a Vector
    # def calc_rad(self, vector_len, movement_vector):
    #     try:
    #         y_val = movement_vector[0] / vector_len
    #         #print("Y_Val", y_val)
    #         return_value = np.arccos(y_val)
    #         return return_value
    #     except TypeError as e:
    #         print("error", e)
    #         raise
    #convert Radian to degree
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
    Active = 1
    GPS_FP = 0


    # initiate Vectors for movement
    __Current_Position = [0, 0]
    __Target_position = []
    __Movement = []  # Movementvector to reach target
    __Angle_to_target = 0

    #when the x, y Current Pos coordinates are close enough so target+offset>pos>target-offset
    __Offset = 0.2

    def thread_wrapper(self):
        while self.Active:
            self.main_logic()

    def main_logic(self):
        try:
            self.plot_course()
            if self.__Angle_to_target == -1:
                self.update_target()
            else:
                self.Writer.set_positon(self.__Angle_to_target)
        except errno:
            print(errno)
            raise errno

    def display_plot(self):
        d = {'Latitude': [self.__Current_Position[0], self.__Target_position[0]],
             'Longitude': [self.__Current_Position[1], self.__Target_position[1]]}
        df = pd.DataFrame(data=d)

        # Plot Graph for easier Display
        BBox = (min(d['Longitude'])-0.002, max(d['Longitude'])+0.002, min(d['Latitude'])-0.002, max(d['Latitude'])+0.002)
        city_map = plt.imread("map.jpg")
        fig, ax = plt.subplots(figsize=(8, 7))
        print(df)
        ax.scatter(df.Longitude, df.Latitude, s=10, c='red', alpha=1)
        ax.set_title('Waypoints Where we need to go')
        ax.set_xlim(BBox[0], BBox[1])
        ax.set_ylim(BBox[2], BBox[3])
        ax.imshow(city_map, zorder=0, extent=BBox)
        plt.show()

    def plot_course(self, should_display=False):
        self.update_position()
        if type(should_display) != bool:
            raise AttributeError
        #print(self.__Current_Position)
        # Calculate the Movement Vector
        try:
            self.__Movement = []
            # Calculate Movement(Velocity) vector
            self.__Movement.append(self.__Target_position[0] - self.__Current_Position[0])
            self.__Movement.append(self.__Target_position[1] - self.__Current_Position[1])

        except IOError as e:
            print("Error: ", e)
            raise
        try:
            movement_length = self.vector_length(self.__Movement)
            movement_normalized = self.vector_normalize(movement_length, self.__Movement)
            print(movement_normalized)
            self.__Angle_to_target = math.atan2(self.__Movement[1],self.__Movement[0])*180/math.pi
            if self.__Angle_to_target < 0:
                self.__Angle_to_target += 360
        except errno:
            print(errno)
        if should_display:
            self.display_plot()
        #self.Active = 0
        if (movement_length < self.__Offset):
            return -1
        print("Angle: ", self.__Angle_to_target)
        return self.__Angle_to_target

