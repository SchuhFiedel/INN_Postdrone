import time
from threading import Thread, Lock
from UdpComms import UdpComms as U

class DataWriter:
    Mutex = Lock()

    def __init__(self, function, args: list):
        self.Function = function
        self.Args = args
        self.Active = True
        self.CurrentPosition = 0.0
        return

    def thread_wrapper(self):
        while self.Active:
            self.Mutex.acquire(blocking=True)
            self.returncode = self.Function(self.Args, self.CurrentPosition)
            self.Mutex.release()
            time.sleep(0.1)

    def send_positional_data(self):
        t = Thread(target=self.thread_wrapper)
        print("Positional Reader with function: " + str(self.Function))
        t.start()

    def set_positon(self, pass_position: float):
        self.Mutex.acquire()
        self.CurrentPosition = pass_position
        self.Mutex.release()

    def deactivate(self):
        self.Active = False


def send_to_UDP(socket: U, dw):
        print(str(dw))
        socket.SendData(str(dw)) # Send this string to other application