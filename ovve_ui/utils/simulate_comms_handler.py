import json
import time
from threading import Thread
from utils.comms_helper import CommsHelper
from utils.params import Params
from utils.settings import Settings


class SimulateCommsHandler():
    def __init__(self, comms_helper: CommsHelper) -> None:
        self.comms_helper = comms_helper
        self.comms_helper.set_comms_handler_callback(self.settings_handler)

    def settings_handler(self, settings_dict: dict) -> None:
        settings = Settings()
        settings.from_dict(settings_dict)
        print("Simulator got new settings from the UI")
        print(settings.to_JSON())


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


