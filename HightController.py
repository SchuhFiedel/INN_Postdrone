
class HeightController:
    def __init__(self, minhight: int):
        __Minimalhight = minhight
        __Currenthight = 0

    def UpdateHight(self , hight):
        __Currenthight = hight

    def IsHightSufficent(self):
        if self.__Currenthight > self.__Minimalhight:
            return True
        return False