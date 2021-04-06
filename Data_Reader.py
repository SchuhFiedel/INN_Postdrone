from abc import ABC

class ReaderInterface:
    @abs
    def read_positional_data(self):
        return


class WebReader(ReaderInterface):
    def read_positional_data(self):
        return
    
    def __init__(self, UDP_Adress, PxPort,RxPort):
        return


class Filereader(ReaderInterface):
    def read_positional_data(self):
        return

    def __init__(self, Filepath, Filename):
        return
