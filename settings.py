import json

# Settings that are sent to MCU


class Settings:
    def __init__(self):
        self.ac_mode = False #mode = True -> AC, mode = False -> SIMV
        self.minute_volume = 0
        self.resp_rate = 0

        # TODO: validate this assumption
        # ie ratio is an enumeration of possible ie ratios
        # ie ratio id is passed from the MCU as an index into the enumeration
        self.ie_ratio_display = ["1:1", "1:1.5", "1:2", "1:3"]
        self.ie_ratio_id = 0


    def set_test_settings(self):
        self.ac_mode = False
        self.minute_volume = 500
        self.resp_rate = 14.0
        self.ie_ratio_id = 0

    def get_ie_display(self):
        if self.ie_ratio_id < len(self.ie_ratio_display):
            return self.ie_ratio_display[self.ie_ratio_id]
        else:
            return "ERROR"

    def to_JSON(self):
        j = {}
        j['ac_mode'] = self.ac_mode
        j['minute_volume'] = self.minute_volume
        j['resp_rate'] = self.resp_rate
        j['ie_ratio_id'] = self.ie_ratio_id
        return json.dumps(j)