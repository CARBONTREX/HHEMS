import logging
import httpx
from dataclasses import dataclass
from ..const import BASE_URL

_LOGGER = logging.getLogger(__name__)

dishwasherJSON = {
    "name": "DishWasher",
    "profile": [[2.343792, 9.91720178381],[0.705584, 8.79153133754],[0.078676, 7.86720661017],[0.078744, 7.87400627016],[0.078948, 7.89440525013],[0.079152, 7.91480423011],[0.079016, 7.90120491012],[0.078812, 7.88080593015],[0.941108, 3.10574286964],[10.449, 18.0981988883],[4.523148, 1.78766247656],[34.157214, 15.5624864632],[155.116416, 70.6731270362],[158.38641, 72.1629803176],[158.790988, 67.6446776265],[158.318433, 72.1320090814],[158.654276, 67.5864385584],[131.583375, 109.033724507],[13.91745, 13.0299198193],[4.489968, 1.91271835851],[1693.082112, 669.148867416],[3137.819256, 447.115028245],[3107.713851, 442.825240368],[3120.197256, 444.604029241],[3123.464652, 445.069607955],[3114.653256, 443.814052026],[3121.27497, 444.757595169],[3116.305863, 444.04953577],[3106.801566, 442.695246796],[3117.703743, 444.248722882],[3118.851648, 444.412290486],[3110.016195, 443.15330662],[3104.806122, 442.410911425],[1148.154728, 416.724520071],[166.342624, 70.8616610914],[161.205252, 68.6731497838],[160.049824, 68.1809395169],[158.772588, 67.6368392593],[158.208076, 67.3963581543],[157.926096, 67.2762351774],[157.01364, 66.8875305491],[112.30272, 108.243298437],[11.65632, 9.35164905552],[17.569056, 18.4299236306],[4.947208, 2.10750178285],[4.724016, 2.012422389],[143.12025, 65.2075123351],[161.129536, 68.6408949029],[160.671915, 63.501604078],[23.764224, 12.8265693277],[136.853808, 62.352437012],[159.11184, 62.8850229849],[159.464682, 63.0244750664],[159.04302, 62.8578235805],[36.68544, 55.7061505818],[9.767628, 7.07164059421],[4.902772, 2.08857212612],[2239.315008, 885.033921728],[3116.846106, 444.126516228],[3111.034014, 443.298337972],[3118.112712, 444.306997808],[3111.809778, 443.408878355],[3113.442189, 443.641484325],[3110.529708, 443.226478259],[3104.676432, 442.392431601],[3101.093424, 441.881880613],[3121.076178, 444.729268843],[1221.232208, 443.248103556],[159.964185, 63.2218912841],[2663.07828, 966.568347525],[272.524675, 436.038267268],[7.76832, 5.82624],[3.258112, 1.75854256572],[3.299408, 1.69033685682],[3.295136, 1.68814824631],[3.256704, 1.75778260783],[3.258112, 1.75854256572],[3.262336, 1.7608224394],[2224.648744, 807.439674778],[367.142872, 587.426961418],[4.711025, 11.8288968082]],
    "timeBase": 60
}

washingmachineJSON = {
    "name": "WashingMachine",
    "profile": [[66.229735, 77.4311402954],[119.35574, 409.21968],[162.44595, 516.545199388],[154.744551, 510.671236335],[177.089979, 584.413201848],[150.90621, 479.851164854],[170.08704, 540.84231703],[134.23536, 460.23552],[331.837935, 783.490514121],[2013.922272, 587.393996],[2032.267584, 592.744712],[2004.263808, 584.576944],[2023.32672, 590.13696],[2041.49376, 595.43568],[2012.8128, 587.0704],[2040.140352, 595.040936],[1998.124032, 582.786176],[2023.459776, 590.175768],[1995.309312, 581.965216],[2028.096576, 591.528168],[1996.161024, 582.213632],[552.525687, 931.898925115],[147.718924, 487.486021715],[137.541888, 490.4949133],[155.996288, 534.844416],[130.246299, 464.477753392],[168.173568, 497.908089133],[106.77933, 380.79103735],[94.445568, 323.813376],[130.56572, 317.819806804],[121.9515, 211.226194059],[161.905679, 360.175184866],[176.990625, 584.085324519],[146.33332, 501.71424],[173.06086, 593.35152],[145.07046, 517.342925379],[188.764668, 522.114985698],[88.4058, 342.394191108],[117.010432, 346.43042482],[173.787341, 326.374998375],[135.315969, 185.177207573],[164.55528, 413.181298415],[150.382568, 515.597376],[151.517898, 540.335452156],[154.275128, 509.122097304],[142.072704, 506.652479794],[171.58086, 490.815333752],[99.13293, 368.167736052],[94.5507, 366.193286472],[106.020684, 378.085592416],[194.79336, 356.012659157],[239.327564, 302.865870739],[152.75808, 209.046388964],[218.58576, 486.26562702],[207.109793, 683.481346289],[169.5456, 581.2992],[215.87571, 712.409677807],[186.858018, 573.073382584],[199.81808, 534.79864699],[108.676568, 403.611655607],[99.930348, 356.366544701],[151.759998, 358.315027653],[286.652289, 300.697988258],[292.921008, 266.244164873],[300.5829, 265.089200586],[296.20425, 261.22759426],[195.74251, 216.883021899],[100.34136, 260.038063655],[312.36975, 275.4842252],[287.90921, 261.688800332],[85.442292, 140.349851956],[44.8647, 109.208529515]],
    "timeBase": 60
}

configJSON = {
  "timeBase": 1,
  "timeDelayBase": 1,
  "timeOffset": -1672585200,
  "timeZone": "Europe/Amsterdam",
  "intervals": 561600,
  "startTime": 1675004400,
  "database": "dem",
  "dataPrefix": "",
  "clearDB": True,
  "extendedLogging": True,
  "logDevices": True,
  "logFlow": True,
  "enablePersistence": False,
  "weatherFile": "data/weather/temperature.csv",
  "irradianceFile": "data/weather/solarirradiation.csv",
  "ventilationFile": "sampledata/singlehouse/Airflow_Profile_Ventilation.csv",
  "gainFile": "sampledata/singlehouse/Heatgain_Profile.csv",
  "dhwFile": "sampledata/singlehouse/Heatdemand_Profile.csv",
  "houseNum": 0,
  "useIslanding": False,
  "photoVoltaicSettings": "sampledata/singlehouse/PhotovoltaicSettings.txt",
  "batterySettings": "sampledata/singlehouse/BatterySettings.txt",
  "heatingSettings": "sampledata/singlehouse/HeatingSettings.txt",
  "useFillMethod": True,
  "usePP": True,
  "ctrlTimeBase": 900,
  "thermostatStartTimes": "sampledata/singlehouse/Thermostat_Starttimes.txt",
  "thermostatSetpoints": "sampledata/singlehouse/Thermostat_Setpoints.txt"
}

@dataclass
class SimDevices:
    """ Class to represent the devices that will be simulated """
    battery: bool
    pv: bool
    dishwasher: bool
    washingmachine: bool

@dataclass
class KnownLoad():
    """ Class to represent the real devices whose consumption is published """
    entity_id: str
    name: str

@dataclass
class UnknownLoad():
    """ Class to represent the real devices whose consumption is not published """
    entity_id: str
    name: str
    consumption: float


def startSim(simDevices: SimDevices, known_loads: list[KnownLoad], unknown_loads: list[UnknownLoad]):
    try:
        with httpx.Client(timeout=10) as client:
            client.post(BASE_URL + "/houses/0").raise_for_status()

            if simDevices.battery:
                client.post(BASE_URL + "/houses/0/battery/Battery", json={"name": "Battery"}).raise_for_status()

            if simDevices.pv:
                client.post(BASE_URL + "/houses/0/solar/PV", json={"name": "PV"}).raise_for_status()

            if simDevices.dishwasher:
                client.post(BASE_URL + "/houses/0/timeshifters/DishWasher", json=dishwasherJSON).raise_for_status()

            if simDevices.washingmachine:
                client.post(BASE_URL + "/houses/0/timeshifters/WashingMachine", json=washingmachineJSON).raise_for_status()

            client.post(BASE_URL + "/houses/0/config", json=configJSON).raise_for_status()

            client.post(BASE_URL + "/houses/0/load").raise_for_status()

            # add read entities
            for load in known_loads:
                client.post(BASE_URL + "/houses/0/entity", json={"entity_id": load.entity_id, "consumption": "-1"}).raise_for_status()

            for load in unknown_loads:
                client.post(BASE_URL + "/houses/0/entity", json={"entity_id": load.entity_id, "consumption": str(load.consumption)}).raise_for_status()

        _LOGGER.info("Simulation started successfully")

        return True
    except Exception as e:
        _LOGGER.error("Error starting simulation: %s", e)

        return False
