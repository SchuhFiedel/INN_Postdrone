from abc import ABC
import UdpComms as U
from threading import Thread, Lock
import concurrent.futures
import time
import io


class Datareader:

    returncode = []

    def __init__(self, function, args):
        self.Function = function
        self.Args = args
        self.Active = True
        return

    def thread_wrapper(self):
        while self.active:
            self.returncode = self.Function(self.Args)
            time.sleep(0.1)

    def read_positional_data(self):
        t = Thread(target=self.thread_wrapper)
        print("Positional Reader with function: " + self.Function)
        t.start()

    def return_positional_data(self):
        return self.returncode

    def deactivate(self):
        self.Active = False


def read_from_UDP(Socket:U.UdpComms):
    data = Socket.ReadReceivedData()  # read data
    if data != None:  # if NEW data has been received since last ReadReceivedData function call
        print(data)  # print new received data
        returnval = data.split(",")
        return returnval
    return None


def read_from_UDP(fp):
    read_string = fp.read()
    read_string = read_string.split(",")
    fp.seek(0)
    return read_string
