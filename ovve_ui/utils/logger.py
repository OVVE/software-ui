""" 
Logging class to save data for debug and analysis
"""
import time
import json
import os

class Logger():
    def __init__(self) -> None:
        self.__enable_console = False
        self.__enable_file = False
        self.__patient_id = "13c50304-5a34-4a39-8665-bde212f2f206"
        self.__path = "/tmp"
        self.__filename = "ovve.log.txt"

    @property
    def enable_console(self) -> bool:
        return self.__enable_console

    @enable_console.setter
    def enable_console(self, value: bool) -> None:
        self.__enable_console = value

    @property
    def enable_file(self) -> bool:
        return self.__enable_file

    @enable_file.setter
    def enable_file(self, value: bool) -> None:
        self.__enable_file = value

    @property
    def patient_id(self) -> str:
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value: str) -> None:
        self.__patient_id = value

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, value: str):
        self.__path = value

    @property
    def filename(self) -> str:
        return self.__filename

    @filename.setter
    def filename(self, value: str):
        self.__filename = value

    def __log_to_console(self, msg: str) -> None:
        print(msg)

    def __log_to_file(self, msg: str) -> None:
        # TODO: This is expensive and we need to evaluate performance.  
        # The logger is stateless so we are opening and closing the log 
        # after each message.  Also, the log messages are verbose and
        # could be much shorter if we eliminate or abbreviate the keys
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        log_fullpath = os.path.join(self.__path, self.__filename)
        try:
            with open(log_fullpath, 'a') as f:
                f.write(msg + "\n")
        except:
            print("Error opening log file " + log_fullpath)


    def log(self, msg_type: str, msg: str) -> None:
        ts = time.time()
        msg_dict = {}
        msg_dict["patient_id"] = self.__patient_id
        msg_dict["ts"] = ts
        msg_dict["type"] = msg_type
        msg_dict["msg"] = msg
        log_msg = json.dumps(msg_dict)

        if self.__enable_console:
            self.__log_to_console(log_msg)
        if self.__enable_file:
            self.__log_to_file(log_msg)