
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


own_position = []
target_position = []
movement = []

try:
    own_position = get_position()
    target_position = get_target()

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
d = {'longitude': [own_position[0], target_position[0]],'latitude': [own_position[1], target_position[1]]}
df = pd.DataFrame(data=d)


BBox = (16.37627, 16.38611, 48.23807, 48.24339)
City_map = plt.imread("map.jpg")
fig, ax = plt.subplots(figsize = (8,7))
print(df)
ax.scatter( df.latitude, df.longitude, s=10, c='red', alpha = 1)
ax.set_title('Waypoints Where Is Where Go')
ax.set_xlim(BBox[0], BBox[1])
ax.set_ylim(BBox[2], BBox[3])
ax.imshow(City_map, zorder=0, extent=BBox)
plt.show()

