 
# Copyright 2020 LifeMech  Inc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, 
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import time
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from utils.Alarm import *
import random
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
        print("P: Ack received from alarm handler")

    def run(self):
        while True:
            for alarmtype in list(AlarmType):
                alarmbits = 0
                alarmbits |= 1 << alarmtype.value
                print("P: Emitting an alarm " + alarmtype.name + " bits: " +
                      str(bin(alarmbits)))
                self.new_alarm_signal.emit(alarmbits)
                time.sleep(random.randrange(0, 3))


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
            num_pending = self.handler.alarms_pending()
            if num_pending > 0:
                print("    C: Alarms pending " + str(num_pending))
                # UI should ask the handler for the highest alarm and display in UI
                highest_alarm = self.handler.get_highest_priority_alarm()
                message = highest_alarm.get_message()
                print("    C: Current highest alarm is " + str(highest_alarm) +
                      " message: " + message)

                # UI should acknowledge the alarm, removing it from the queue
                print("    C: Acknowledging the alarm")
                self.handler.acknowledge_alarm(highest_alarm)
            time.sleep(random.randrange(0, 3))


if __name__ == '__main__':
    import sys
    app = QtCore.QCoreApplication(sys.argv)
    handler = AlarmHandler()
    alarm_emitter = AlarmEmitter(handler)
    alarm_consumer = AlarmConsumer(handler)
    sys.exit(app.exec_())
