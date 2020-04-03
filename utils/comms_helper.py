"""
Glue between comms library and UI
"""
from typing import Callable
from utils.params import Params
from utils.settings import Settings
import json

class CommsHelper():
    def __init__(self) -> None: 
        self.ui_callback = None
        self.settings_callback = None

    # Sets the function in the UI that gets called whenever 
    # params are updated.
    def set_ui_callback(self, 
        ui_callback: Callable[[Params], None]) -> None:
        self.ui_callback = ui_callback

    # Sets the function in the comms handler that gets called
    # whenever settings are updated
    def set_settings_callback(self,
        settings_callback : Callable[[str], None]) -> None:
        self.settings_callback = settings_callback

    def settings_handler(self, settings: Settings) -> None:
        print("Got new settings from the UI")
        print(settings.to_JSON)

        # Serialize or convert settings into form usable by 
        # comms handler
        # Call comms handler callback with new settings
        if settings_callback:
            settings_callback(settings.to_JSON())
        else:
            print("Got new settings but no comms handler callback!")


    def params_handler(self, 
        params_from_comms: dict) -> None:
        params = Params()
        params.from_dict(params_from_comms)

        # Deserialize or otherwise handle params
        # coming in from the comms handler
        print("Got new params from the comms handler")
        print(params.to_JSON())

        # Call the callback provided by the UI
        if self.ui_callback:
            self.ui_callback(params)
        else:
            print("Got new params but no UI callback!")

    