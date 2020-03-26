import json

class AqualungSettings:
    def __init__(self):
        self.__ac = True
        self.__simv = True
        self.__bpm = 0
        self.__tv = 0
        self.__ie = 0
        self.__fio2 = 0

    @property
    def ac(self):
        return self.__ac

    @ac.setter
    def ac(self, value):
        self.__ac = value

    @property
    def simv(self):
        return self.__simv

    @simv.setter
    def simv(self, value):
        self.__simv = value

    @property
    def bpm(self):
        return self.__bpm

    @bpm.setter
    def bpm(self, value):
        self.__bpm = value

    @property
    def tv(self):
        return self.__tv

    @tv.setter
    def tv(self, value):
        self.__tv = value

    @property
    def ie(self):
        return self.__ie

    @ie.setter
    def ie(self, value):
        self.__ie = value

    @property
    def fio2(self):
        return self.__fio2

    @fio2.setter
    def fio2(self, value):
        self.__fio2 = value


    def toJSON(self):
        j = {}
        j['ac'] = self.__ac
        j['simv'] = self.__simv
        j['bpm'] = self.__bpm
        j['tv'] = self.__tv
        j['ie'] = self.__ie
        j['fio2'] = self.__fio2

        return json.dumps(j)