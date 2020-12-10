import os.path
import os
import errno


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
            # Not a permission error.
        raise
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

    movement.append( target_position[0] - own_position[0])
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
