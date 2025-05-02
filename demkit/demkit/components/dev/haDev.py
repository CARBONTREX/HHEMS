from demkit.components.dev.device import Device
# from demkit.components.device import Device

import random
import requests

class HADev(Device):
    def __init__(self, name, host, baseURL, endpoint):
        super().__init__(name, host)

        self.baseURL = baseURL
        self.endpoint = endpoint

    def timeTick(self, time, deltatime=0):

        self.lockState.acquire()

        response = requests.get(self.baseURL + self.endpoint)

        if not response.ok:
            print("Error: " + str(response.status_code))
            self.lockState.release()
            return

        consumption = float(response.json()['consumption'])


        for c in self.commodities:
            self.consumption[c] = complex(consumption, 0)

        self.lockState.release()