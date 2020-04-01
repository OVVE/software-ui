import json


class AqualungSettings():
    def __init__(self):
        self.__mode = False #mode = True -> AC, mode = False -> SIMV
        self.__peep = 0
        self.__bpm = 0
        self.__tv = 0
        self.__ie = 0
        self.__fio2 = 0
        self.__resp_rate = 0
        self.__peak_press = 0 #value comes from sensor
        self.__plateau_press = 0 #value comes from sensor

    @property
    def peep(self):
        return self.__peep

    @peep.setter
    def peep(self, value):
        self.__peep = value

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        self.__mode = value

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

    @property
    def resp_rate(self):
        return self.__resp_rate

    @resp_rate.setter
    def resp_rate(self, value):
        self.__resp_rate = value

    @property
    def peak_press(self):
        return self.__peak_press

    @peak_press.setter
    def peak_press(self, value):
        self.__peak_press = value

    @property
    def plateau_press(self):
        return self.__plateau_press

    @plateau_press.setter
    def plateau_press(self, value):
        self.__plateau_press = value

    def toJSON(self):
        j = {}
        j['peep'] = self.__peep
        j['mode'] = self.__mode
        j['tv'] = self.__tv
        j['ie'] = self.__ie
        j['fio2'] = self.__fio2
        j['resp_rate'] = self.__resp_rate
        j['peak_press'] = self.__peak_press
        j['plateau_press'] = self.__plateau_press

        return json.dumps(j)
