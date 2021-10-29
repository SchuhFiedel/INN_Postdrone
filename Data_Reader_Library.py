import UdpComms as U
from threading import Thread, Lock
import time
import CustomExceptions


class DataReader:

    returncode = []
    Mutex = Lock()

    def __init__(self, function, args):
        self.Function = function
        self.Args = args
        self.Active = True
        return

    def thread_wrapper(self):
        while self.Active:
            self.Mutex.acquire(blocking=True)
            self.returncode = self.Function(self.Args)
            self.Mutex.release()
            time.sleep(0.1)

    def read_positional_data(self):
        t = Thread(target=self.thread_wrapper)
        print("Positional Reader with function: " + str(self.Function))
        t.start()

    def return_positional_data(self):
        self.Mutex.acquire()
        tmp = self.returncode
        self.Mutex.release()
        if len(tmp) != 3:
            raise CustomExceptions.PositionalFormat
        return tmp

    def deactivate(self):
        self.Active = False


def cast_list(test_list, data_type):
    return list(map(data_type, test_list))


def read_from_udp(socket: U.UdpComms):
    data = socket.ReadReceivedData()  # read data
    if (
        data is not None
    ):  # if NEW data has been received since last ReadReceivedData function call
        # print(data)  # print new received data
        return_value = data.split(",")
        return cast_list(return_value, float)
    return None


def read_from_file(fp):
    try:
        read_string = fp.read()
        read_string = read_string.split(",")
        return cast_list(read_string, float)
    except:
        raise FileNotFoundError


def read_from_console():
    try:
        val1 = float(input("Enter Longitude "))
        val2 = float(input("Enter Lattitude "))
        return_value = [val1, val2]
        return return_value
    except:
        raise TypeError
