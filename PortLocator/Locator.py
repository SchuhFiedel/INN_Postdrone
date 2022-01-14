import glob
from os import listdir
from os.path import isfile, join
from dronekit import connect
dev_folder = './dev/ttyS*'

FileGlob = glob.glob(dev_folder)
print("Hier Sollte eine Liste an Objekten sein")
print(FileGlob)
for file in FileGlob:
    try:
        # Connect to the Vehicle (in this case a UDP endpoint)
        vehicle = connect(file, wait_ready=True, baud=57600, heartbeat_timeout=10)
        print("HEARTHBEAT FROM " + file)
        print("GPS LOCATION:")
        print(vehicle.location.global_relative_frame)

        exit()
    except:
        print("NO HEARTHBEAT IN 10 SECONDS FROM" + file)

