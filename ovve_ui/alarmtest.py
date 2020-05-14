import time
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from utils.Alarm import *

'''
  Simulates what should happen in comms handler
'''
class AlarmEmitter(QtCore.QThread):
    new_alarm_signal = pyqtSignal(int)

    def __init__(self, handler: AlarmHandler):
        super().__init__()
        self.handler = handler
        self.new_alarm_signal.connect(self.handler.set_active_alarms)
        self.handler.acknowledge_alarm_signal.connect(self.handle_ack)
        self.start()

    def handle_ack(self):
        print("Ack received from alarm handler")

    def run(self):
        while True:  
            for alarmtype in list(AlarmType):
                alarmbits = 0
                alarmbits |= 1 << alarmtype.value      
                print("Emitting an alarm " + alarmtype.name + " bits: " + str(bin(alarmbits)))
                self.new_alarm_signal.emit(alarmbits)
                time.sleep(1)
            
'''
  Simulates what should happen in UI
'''
class AlarmConsumer(QtCore.QThread):
    def __init__(self, handler: AlarmHandler):
        super().__init__()
        self.handler = handler
        self.start()

    def run(self):
        while True:  
            if self.handler.alarm_is_pending():
                highest_alarm = self.handler.get_highest_priority_alarm()
                message = highest_alarm.get_message()
                print("Current highest alarm is " + str(highest_alarm) + " message: " + message)
                print("Consumer acknowledging the alarm")
                self.handler.acknowledge_current_alarm()


if __name__ == '__main__':
    import sys
    app = QtCore.QCoreApplication(sys.argv)
    handler = AlarmHandler()
    alarmemitter = AlarmEmitter(handler)
    alarmconsumer = AlarmConsumer(handler)
    sys.exit(app.exec_())