"""
Glue between comms library and UI
"""
import json
from typing import Callable

from utils.params import Params
from utils.settings import Settings
from utils.alarms import Alarms
from utils.logger import Logger


class CommsAdapter():
    def __init__(self, logger: Logger) -> None:
        self.ui_params_callback = None
        self.ui_alarms_callback = None
        self.comms_callback = None
        self.logger = logger

    # Sets the function in the UI that gets called whenever
    # params are updated.
    def set_ui_params_callback(self, ui_params_callback: Callable[[Params], None]) -> None:
        self.ui_params_callback = ui_params_callback

    # Sets the function in the UI that gets called whenever
    # alarms are updated.
    def set_ui_alarms_callback(self, ui_alarms_callback: Callable[[Alarms], None]) -> None:
        self.ui_alarms_callback = ui_alarms_callback

    # Sets the function in the comms handler that gets called
    # whenever settings are updated
    def set_comms_callback(self, comms_callback: Callable[[dict],
                                                          None]) -> None:
        self.comms_callback = comms_callback

    def update_settings(self, settings: Settings) -> None:
        # Serialize or convert settings into form usable by
        # comms handler
        # Call comms handler callback with new settings
        if self.comms_callback:
            settings_str = settings.to_JSON()
            self.logger.log("settings,", settings_str)
            j = json.loads(settings_str)
            self.comms_callback(j)
        else:
            print("No comms callback!")

    def update_params(self, params_from_comms: dict) -> None:
        params = Params()
        params.from_dict(params_from_comms)

        # Deserialize or otherwise handle params
        # coming in from the comms handler
        self.logger.log("params", params.to_JSON())

        # Call the callback provided by the UI
        if self.ui_params_callback:
            self.ui_params_callback(params)
        else:
            print("No UI params callback!")


    def update_alarms(self, alarms_from_comms: dict) -> None:
        alarms = Alarms()
        alarms.from_dict(alarms_from_comms)

        # Deserialize or otherwise handle params
        # coming in from the comms handler
        self.logger.log("alarms", alarms.to_JSON())

        # Call the callback provided by the UI
        if self.ui_alarms_callback:
            self.ui_alarms_callback(alarms)
        else:
            print("No UI alarms callback!")