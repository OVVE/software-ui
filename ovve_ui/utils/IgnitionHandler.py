from logging import StreamHandler
import requests
import gc
import json

class IgnitionHandler(StreamHandler):

    def __init__(self, patientID, messageType):

        StreamHandler.__init__(self)

        if messageType == 'DATA':
            self.httpEndpointURL = "http://40.76.28.105:8088/system/webdev/LifeMech/post_OVVE_Data"
        else:
            self.httpEndpointURL = "http://40.76.28.105:8088/system/webdev/LifeMech/post_Alarm_Data"

        self.patientID = str(patientID)

    def emit(self, record):

        try:

            msg = self.format(record)
            url = self.httpEndpointURL

            patient_id_key = {"patient_id": self.patientID}

            msg = json.loads(msg)
            msg.update(patient_id_key)
            msg = json.dumps(msg)

            #print(msg)

            gc.collect()

            response = requests.post(url, json=msg)
            #print(response.text)

        except:
            print('Error while sending data to Ignition.')
            pass
