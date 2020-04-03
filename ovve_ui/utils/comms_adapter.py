"""
Glue between comms library and UI
"""
import json
from typing import Callable

from utils.params import Params
from utils.settings import Settings


class CommsAdapter():
    def __init__(self) -> None:
        self.ui_callback = None
        self.comms_callback = None

    # Sets the function in the UI that gets called whenever
    # params are updated.
    def set_ui_callback(self, ui_callback: Callable[[Params], None]) -> None:
        self.ui_callback = ui_callback

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
            j = json.loads(settings_str)
            self.comms_callback(j)
        else:
            print("No comms callback!")
            
    def update_params(self, params_from_comms: dict) -> None:
        params = Params()
        params.from_dict(params_from_comms)

        # Deserialize or otherwise handle params
        # coming in from the comms handler
        print("Got updated params from comms")
        print(params.to_JSON())

        # Call the callback provided by the UI
        if self.ui_callback:
            self.ui_callback(params)
        else:
            print("No UI callback!")
