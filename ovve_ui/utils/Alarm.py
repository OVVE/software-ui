import time
from enum import Enum
from queue import PriorityQueue
from typing import List
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from threading import RLock

'''
  Encode the alarms in the enum in bit order according to v0.35
'''
class AlarmType(Enum):
    AC_POWER_LOSS = 0
    LOW_BATTERY  = 1
    BAD_PRESSURE_SENSOR = 2
    BAD_FLOW_SENSOR = 3
    ECU_COMMS_FAILURE = 4
    ECU_HARDWARE_FAILURE = 5
    ESTOP_PRESSED = 6
    HIGH_PRESSURE = 8
    LOW_PRESSURE = 9
    HIGH_VOLUME = 10
    LOW_VOLUME = 11
    HIGH_RESP_RATE = 12
    LOW_RESP_RATE = 13
    UI_COMMS_FAILURE = 16
    UI_HARDWARE_FAILURE = 17
    SETPOINT_MISMATCH = 24

class Alarm():
    messages : dict = {
        AlarmType.AC_POWER_LOSS: "AC Power is disconnected",
        AlarmType.LOW_BATTERY: "Battery reaches 20% or less",
        AlarmType.BAD_PRESSURE_SENSOR: "A problem has been detected in the pressure sensing circuit",
        AlarmType.BAD_FLOW_SENSOR: "A problem has been detected in the flow sensing circuit",
        AlarmType.ECU_COMMS_FAILURE: "Communications are too unreliable to operate",
        AlarmType.ECU_HARDWARE_FAILURE: "A hardware failure has been detected",
        AlarmType.ESTOP_PRESSED: "Emergency stop button has been pressed",
        AlarmType.HIGH_PRESSURE: "Pressure exceeded the high pressure limit",
        AlarmType.LOW_PRESSURE: "Pressure is below the low pressure limit",
        AlarmType.HIGH_VOLUME: "Volume IN detected exceeding the high volume limit",
        AlarmType.LOW_VOLUME: "Volume IN detected exceeding the low volume limit",
        AlarmType.HIGH_RESP_RATE: "Respiratory rate exceeded the high rate limit",
        AlarmType.LOW_RESP_RATE: "Respiratory rate below the low rate limit",
        AlarmType.UI_COMMS_FAILURE: "Communications are too unreliable to operate",
        AlarmType.UI_HARDWARE_FAILURE: "A hardware failure has been detected",
        AlarmType.SETPOINT_MISMATCH: "One or more setpoints does not match between UI and ECU"
    }

    def __init__(self, alarm_type: AlarmType):
        self.time = time.time()
        self.alarm_type = alarm_type

    def get_message(self) -> str:
        return self.messages.get(self.alarm_type, "")

    def __lt__(self, other):
        return self.time < other.time
    
    def __eq__(self, other):
        if self.time == other.time and self.alarm_type == other.alarm_type:
            return True
        return False

class AlarmQueue(List): 
    priorities : dict = {
        AlarmType.AC_POWER_LOSS: 0,
        AlarmType.LOW_BATTERY : 1,
        AlarmType.BAD_PRESSURE_SENSOR: 2,
        AlarmType.BAD_FLOW_SENSOR: 3,
        AlarmType.ECU_COMMS_FAILURE: 4,
        AlarmType.ECU_HARDWARE_FAILURE: 5,
        AlarmType.ESTOP_PRESSED: 6,
        AlarmType.HIGH_PRESSURE: 7,
        AlarmType.LOW_PRESSURE: 8,
        AlarmType.HIGH_VOLUME: 9,
        AlarmType.LOW_VOLUME: 10,
        AlarmType.HIGH_RESP_RATE: 11,
        AlarmType.LOW_RESP_RATE: 12,
        AlarmType.UI_COMMS_FAILURE: 13,
        AlarmType.UI_HARDWARE_FAILURE: 14,
        AlarmType.SETPOINT_MISMATCH: 15,
    }

    def __init__(self) -> None:
        super().__init__()
 
    
    def put(self, alarm: Alarm):
        # If the alarm is already in the queue, do nothing
        try:
            index(alarm)
        except:
            priority = self.priorities.get(alarm.alarm_type)
            super().append((priority, alarm))
            super().sort()

    def peek(self) -> Alarm:
        if len(self) > 0:
            tup = self[0]
            return tup[1]
        else:
            return None

    def get(self) -> Alarm:
        tup = super().get()
        return tup[1]

    def index(self, alarm) -> int:
        priority = self.priorities.get(alarm.alarm_type)
        return super().index((priority, alarm))

    def remove(self, alarm):
        priority = self.priorities.get(alarm.alarm_type)
        super().remove((priority, alarm))

    def num_pending(self) -> int:
        return len(self)
        
class AlarmHandler(QtCore.QObject):
    acknowledge_alarm_signal = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self._active_alarmbits = 0
        self._ack_alarmbits = 0
        self._alarm_queue = AlarmQueue()
        self._lock = RLock()
        

    '''
     This function should be connected to a signal emitted
     by the comms handler when alarm bits are received
    '''
    def set_active_alarms(self, alarmbits: int) -> None:
        self._lock.acquire()
    
        self._active_alarmbits = alarmbits
        
        # Iterate through the bits and set all active alarms
        pos = 0
        while (pos < 32):
            bit = alarmbits & 1
            if bit == 1:
                try:
                    alarmtype = AlarmType(pos)
                    self._set_alarm(alarmtype)
                except ValueError:
                    print("Got invalid alarm bit at pos " + str(pos))
            alarmbits = alarmbits >> 1
            pos += 1

        # Zero the ack bits that are no longer active
        self._ack_alarmbits &= self._active_alarmbits
       
        self._lock.release()
    
    '''
      This function is called by the UI to retrieve highest
      priority unacknowledged alarm
    '''
    def get_highest_priority_alarm(self) -> Alarm:
        self._lock.acquire()
        alarm = self._alarm_queue.peek()
        self._lock.release()
        return alarm

    '''
     This function should be called by the UI when it
     acknowledges the current alarm.  
    '''
    def acknowledge_alarm(self, alarm) -> None:
        self._lock.acquire()
        try:
            # Make sure the alarm is in the queue
            self._alarm_queue.index(alarm)
            self._alarm_queue.remove(alarm)
            alarmbit = alarm.alarm_type.value
            self._ack_alarmbits |= 1 << alarmbit
            self.acknowledge_alarm_signal.emit(self._ack_alarmbits)
        except:
            print("Error acknowledging alarm: " + str(alarm))
       
        self._lock.release()
        

    def alarms_pending(self) -> int:
        self._lock.acquire()
        num_pending = self._alarm_queue.num_pending()
        self._lock.release()
        return num_pending


    def _set_alarm(self, alarm_type: AlarmType) -> None:
        self._lock.acquire()
        alarm = Alarm(alarm_type)
        self._alarm_queue.put(alarm)
        self._lock.release()

