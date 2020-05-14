import time
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from utils.Alarm import *

'''
  Simulates what should happen in comms handler
'''
class AlarmEmitter(QtCore.QThread):
    new_alarm_signal = pyqtSignal(bytearray)

    def __init__(self, handler: AlarmHandler):
        super().__init__()
        self.handler = handler
        self.new_alarm_signal.connect(self.handler.set_alarms)
        self.handler.acknowledge_alarm_signal.connect(self.handle_ack)
        self.start()

    def handle_ack(self):
        print("Ack received from alarm handler")

    def run(self):
        count = 0
        while True:  
            print("Emitting an alarm")
            alarm_bytes = bytearray(5)
            alarm_bytes[4] = count
            self.new_alarm_signal.emit(alarm_bytes)
            count += 1
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
            if self.handler.is_alarm_pending():
                highest_alarm = self.handler.get_highest_priority_alarm()
                message = highest_alarm.get_message()
                print("Got an alarm from the queue " + str(highest_alarm) + " message: " + message)
                print("Consumer acknowledging the alarm")
                self.handler.acknowledge_alarm(highest_alarm)


if __name__ == '__main__':
    import sys
    app = QtCore.QCoreApplication(sys.argv)
    handler = AlarmHandler()
    alarmemitter = AlarmEmitter(handler)
    alarmconsumer = AlarmConsumer(handler)
    sys.exit(app.exec_())