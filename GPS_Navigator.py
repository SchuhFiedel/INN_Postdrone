import errno
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from threading import Thread, Lock
import time

#Merken, 1ster Wert = Y, 2ter Wert = x für GPS
class Navigator:

    def __init__(self):
        self.Target_position = self.update_target()
        self.GPS_FP = open("GPS_Interface.txt", "r")
        #self.Update_Thread = Thread(target=self.loop_update_target())
        #self.Update_Thread.start()

    def loop_update_target(self):
        while self.Active == 1:
            self.Mutex.acquire()
            self.update_target()
            self.Mutex.release()
            time.sleep(0.1)

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
            current_position_string = self.GPS_FP.read()
            x_local_position, y_local_position = current_position_string.split(',')
            return_value = [float(x_local_position), float(y_local_position)]
            return return_value
        except IOError as e:
            print("error")
            if e.errno == errno.EACCES:
                return "some default data"
                # Not a permission error.
            raise e
        finally:
            self.GPS_FP.seek(0)

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

    def vector_normalize(self, vector_len, vector):
        try:
            return_values = []
            for number in vector:
                return_values.append(number / vector_len)
            return return_values
        except:
            print("error")

            raise

    def calc_rad(self, vector_len, movement_vector):
        try:
            y_val = movement_vector[0] / vector_len
            print("Y_Val", y_val)
            return_value = np.arccos(y_val)
            return return_value
        except TypeError as e:
            print("error", e)
            raise

    def rad_to_ang(self, vector_rad, movement_vector):
        try:
            returnval = np.rad2deg(vector_rad)
            if movement_vector[1] < 0:
                returnval = abs(returnval - 360)
            #Wenn wir mir Einheitskreis rechenn dann muss der Returnval + 90 modulo 360
            return returnval
        except TypeError as e:
            print("error", e)
            raise

    #general program object
    Active = 1
    GPS_FP = 0
    Update_Thread = 0
    Mutex = Lock()

    #initiate Vectors for movement
    Own_position = []
    Target_position = []
    Movement = [] #Movementvector to reach target
    Angle_to_target = 0

    def display_plot(self):
        d = {'Latitude': [self.Own_position[0], self.Target_position[0]],
             'Longitude': [self.Own_position[1], self.Target_position[1]]}
        df = pd.DataFrame(data=d)

        # Plot Graph for easier Display
        BBox = (16.37627, 16.38611, 48.23807, 48.24339)
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
        if type(should_display) != bool:
            raise AttributeError

        # Calculate the Movement Vector
        try:
            # fetch Position and targets
            self.Own_position = self.update_position()

            # Calculate Movement(Velocity) vector
            self.Movement.append(self.Target_position[0] - self.Own_position[0])
            self.Movement.append(self.Target_position[1] - self.Own_position[1])

            if self.Movement[0] + self.Movement[1] == 0:
                print("Error: Values match, no movement possible")
                exit()

            if self.Movement[0] > 0:
                x_direction = 'n'
            else:
                x_direction = 's'

            if self.Movement[1] > 0:
                y_direction = 'e'
            else:
                y_direction = 'w'

            print("Drone need to go: ", x_direction + y_direction, " Position: ", self.Own_position, self.Target_position, self.Movement)

        except IOError as e:
            print("Error: ", e)
            raise

        # Create Pandas DF for Display

        # Calculate Length and Normalize vector
        try:
            print(self.Movement)
            movement_length = self.vector_length(self.Movement)
            print("VectorLength: ", type(movement_length), " ", movement_length)
            movement_normalized = self.vector_normalize(movement_length, self.Movement)
            print(movement_normalized)
            print(movement_normalized[0] * movement_length)
            movement_radiant = self.calc_rad(movement_length, self.Movement)
            print("Radiant: ", movement_radiant)
            movement_angle = self.rad_to_ang(movement_radiant, self.Movement)

            print("Angle: ", movement_angle)
            self.Angle_to_target = movement_angle
        except:
            print("error found")
        if should_display:
            self.display_plot()


A = Navigator()
A.plot_course(should_display=True)
