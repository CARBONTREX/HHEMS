from typing import Optional
from .const import BASE_URL
from .model.measurement import Measurement
from .model.battery_info import BatteryInfo
from .model.solar_info import SolarInfo
from .model.rest_error import RestError
from .model.thermal_info import ThermalInfo
import requests


def _get_measurement(path: str) -> Measurement:
    resp = requests.get(BASE_URL + path, timeout=5)
    data = resp.json()

    # check if data has a unit key
    if "unit" not in data or "value" not in data:
        raise RestError("Invalid data format")

    return Measurement(value=float(data["value"]), unit=data["unit"])


def _get_battery_info(path: str) -> BatteryInfo:
    resp = requests.get(BASE_URL + path, timeout=5)
    data = resp.json()

    return BatteryInfo(
        capacity=data["capacity"],
        max_charge=data["max_charge"],
        max_discharge=["max_discharge"],
        state_of_charge=data["state_of_charge"],
        target_soc=data["target_soc"],
        status=data["status"],
        consumption=data["consumption"],
    )

def _get_solar_info(path: str) -> SolarInfo:
    resp = requests.get(BASE_URL + path, timeout=5)
    data = resp.json()

    return SolarInfo(
        consumption=data["consumption"],
    )

def _set_solar_state(path: str, state: bool) -> None:
    requests.get(BASE_URL + path + '/toggle/' + str(state).lower(), timeout=5)

def _set_target_soc(path: str, target: Optional[float]) -> None:
    if target is None:
        requests.get(BASE_URL + path + '/target', timeout=5)
    else:
        requests.get(BASE_URL + path + '/target/' + str(target), timeout=5)


def _get_thermal_info(path: str) -> ThermalInfo:
    resp = requests.get(BASE_URL + path, timeout=5)
    data = resp.json()

    return ThermalInfo(
        consumption=data["consumption"],
        current_temperature=data["current_temperature"],
        target_temperature=data["target_temperature"],
        heating_power=data["heating_power"],
    )

def _set_target_temp(path: str, temp: float) -> None:
    requests.get(BASE_URL + path + '/target/' + str(temp), timeout=5)