import json
import random
import time
from threading import Thread

from utils.comms_adapter import CommsAdapter
from utils.params import Params
from utils.settings import Settings


class CommsSimulator():
    def __init__(self, comms_adapter: CommsAdapter) -> None:
        self.comms_adapter = comms_adapter
        self.comms_adapter.set_comms_callback(self.update_settings)

    def update_settings(self, settings_dict: dict) -> None:
        settings = Settings()
        settings.from_dict(settings_dict)
        print("Got updated settings from UI")
        print(settings.to_JSON())

    def simulate_params(self) -> None:
        params = Params()
        params_str = params.to_JSON()
        params_dict = json.loads(params_str)

        while True:
            params_dict["peep"] = random.randrange(3, 6)
            params_dict["tv_insp"] = random.randrange(475, 575)
            params_dict["tv_exp"] = random.randrange(475, 575)
            params_dict["ppeak"] = random.randrange(15, 20)
            params_dict["pplat"] = random.randrange(15, 20)
            self.comms_adapter.update_params(params_dict)
            time.sleep(1)

    def start(self) -> None:
        t = Thread(target=self.simulate_params, args=())
        t.start()
