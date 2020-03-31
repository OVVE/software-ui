import json 

# Read only params from the MCU

class Params:
    def __init__(self):
        self.peep = 0
        self.tv_insp = 0
        self.tv_exp = 0
        self.ppeak = 0
        self.pplat = 0

    def set_test_params(self):
        self.peep = 5
        self.tv_insp = 435
        self.tv_exp = 340
        self.ppeak = 20
        self.pplat = 2.5
        
    def to_JSON(self):
        j = {}
        j['peep'] = self.peep
        j['tv_insp'] = self.tv_insp
        j['tv_exp'] = self.tv_exp
        j['ppeak'] = self.ppeak
        j['pplat'] = self.pplat
        return json.dumps(j)