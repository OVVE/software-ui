import time
from enum import Enum
from queue import PriorityQueue
from typing import List
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from threading import Lock

class AlarmType(Enum):
    LOW_PRESSURE = 1
    HIGH_PRESSURE = 2

class Alarm():
    messages : dict = {
        AlarmType.LOW_PRESSURE: "Low pressure warning!",
        AlarmType.HIGH_PRESSURE: "High pressure warning!"
    }

    def __init__(self, alarm_type: AlarmType):
        self.timefired = time.time()
        self.alarm_type = alarm_type

    def get_message(self) -> str:
        return self.messages.get(self.alarm_type, "")


class AlarmQueue(PriorityQueue): 
    priorities : dict = {
        AlarmType.LOW_PRESSURE: 100,
        AlarmType.HIGH_PRESSURE: 200
    }

    def __init__(self) -> None:
        super().__init__()
 
    
    def put(self, alarm: Alarm):
        # TODO: Check and see if alarm is already in the queue 
        # before adding a new entry
        super().put((self.priorities.get(alarm.alarm_type), alarm))

    def get(self) -> Alarm:
        tup = super().get()
        return tup[1]

class AlarmHandler(QtCore.QObject):
    acknowledge_alarm_signal = pyqtSignal(bytearray)

    def __init__(self) -> None:
        super().__init__()
        self.alarm_queue = AlarmQueue()
        
    '''
     This function should be connected to a signal emitted
     by the comms handler when alarm bits are received
    '''
    def set_alarms(self, alarm_bytes: bytearray) -> None:
        print("Alarm handler got alarm bytes " + str(alarm_bytes))
        
        # TODO: Parse bytes and enqueue alarms
        # parse alarm bits and add alarms to the priority queue
        # Ex.  e got a low pressure alarm
        self.__enqueue_alarm(AlarmType.LOW_PRESSURE)

    '''
     This function should be called by the UI when it
     acknowledges an alarm.  It emits a signal that is
     handled by comms to send the bytes back to the MCU
    '''
    def acknowledge_alarm(self, alarm: Alarm):
        # Create a byte array for acknowledged alarms
        # Emit a signal that will be received by the comms handler

        # TODO: Convert alarm to bytes
        ackbytes = bytearray(5)
        self.acknowledge_alarm_signal.emit(ackbytes)


    '''
      This function is called by the UI to retrieve the
      highest priority alarm in the queue
    '''
    def get_highest_priority_alarm(self) -> Alarm:
        return self.alarm_queue.get()
        
    def is_alarm_pending(self) -> bool:
        return self.alarm_queue.empty()

    def __enqueue_alarm(self, alarm_type: AlarmType) -> None:
        alarm = Alarm(alarm_type)
        self.alarm_queue.put(alarm)

 

    