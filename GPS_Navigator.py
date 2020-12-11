import errno
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_target():
    try:
        f = open("Target.txt", "r")
        current_position_string = f.read()
        x_local_position, y_local_position = current_position_string.split(',')
        return_value = [float(x_local_position), float(y_local_position)]
        return return_value
    except IOError as e:
        print("error")
        if e.errno == errno.EACCES:
            return "some default data"
        raise e
    finally:
        f.close()


def get_position():
    try:
        f = open("GPS_Interface.txt", "r")
        current_position_string = f.read()
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
        f.close()


def vector_length(vector=[]):
    try:
        sumation = 0
        for number in vector:
            sumation = sumation + number*number

        sumation = np.sqrt(sumation)
        return sumation
    except:
        print("error")

        raise


def vector_normalize(vector_len, vector=[]):
    try:
        return_values = []
        for number in vector:
            return_values.append(number/vector_len)
        return return_values
    except:
        print("error")

        raise


def calc_rad(vector_len, movement_vector=[]):
    try:
        y_val = movement_vector[0]/vector_len
        print("Y_Val", y_val)
        return_value = np.arccos(y_val)
        return return_value
    except TypeError as e:
        print("error", e)
        raise


def rad_to_ang(vector_rad, movement_vector=[]):
    try:
        returnval = np.rad2deg(vector_rad)
        if movement_vector[1] < 0:
            returnval = abs(returnval - 360)
        #Wenn wir mir Einheitskreis rechenn dann muss der Returnval + 90 module 360
        return returnval
    except TypeError as e:
        print("error", e)
        raise


#initiate Vectors
own_position = []
target_position = []
movement = []

#Calculate the Movement Vector
try:
    #fetch Position and targets
    own_position = get_position()
    target_position = get_target()

    #Calculate Movement(Velocity) vector
    movement.append(target_position[0] - own_position[0])
    movement.append(target_position[1] - own_position[1])

    if movement[0] > 0:
        x_direction = 'n'
    else:
        x_direction = 's'

    if movement[1] > 0:
        y_direction = 'e'
    else:
        y_direction = 'w'

    print("Drone need to go: ", x_direction + y_direction, " Position: ", own_position, target_position, movement)

except IOError as e:
    print("Error: ", e)
    exit

#Create Pandas DF for Display

d = {'Latitude': [own_position[0], target_position[0]], 'Longitude': [own_position[1], target_position[1]]}
df = pd.DataFrame(data=d)

#Plot Graph for easier Display
BBox = (16.37627, 16.38611, 48.23807, 48.24339)
City_map = plt.imread("map.jpg")
fig, ax = plt.subplots(figsize=(8, 7))
print(df)
ax.scatter(df.Longitude, df.Latitude, s=10, c='red', alpha = 1)
ax.set_title('Waypoints Where we need to go')
ax.set_xlim(BBox[0], BBox[1])
ax.set_ylim(BBox[2], BBox[3])
ax.imshow(City_map, zorder=0, extent=BBox)
#plt.show()

#Calculate Length and Normalize vector
try:
    print(movement)
    movement_length = vector_length(movement)
    print("VectorLength: ", type(movement_length), " ", movement_length)
    movement_normalized = vector_normalize(movement_length, movement)
    print(movement_normalized)
    print(movement_normalized[0]*movement_length)
    movement_radiant = calc_rad(movement_length, movement)
    print("Radiant: ", movement_radiant)
    movement_angle = rad_to_ang(movement_radiant, movement)

    print("Angle: ", movement_angle)

except:
    print("error found")
