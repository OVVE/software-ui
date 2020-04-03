import json
import time
from threading import Thread
from utils.comms_helper import CommsHelper
from utils.params import Params


class SimulateCommsHandler():
    def __init__(self, comms_helper: CommsHelper) -> None:
        self.comms_helper = comms_helper
        #comms_helper.set_settings_callback(self.setings_handler)

    def simulate_params(self) -> None:
        params = Params()
        params.set_test_params()
        params_str = params.to_JSON()
        params_dict = json.loads(params_str)

        while True:
            params_dict["tv_insp"] += 1
            self.comms_helper.params_handler(params_dict)
            time.sleep(1)

    def start(self) -> None:
            t = Thread(target=self.simulate_params, args=())
            t.start()