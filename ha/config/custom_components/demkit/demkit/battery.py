from typing import Optional
from custom_components.hemsdelft.demkit.model.battery_info import BatteryInfo
from .rest import _get_battery_info, _set_target_soc

def get_battery_info() -> BatteryInfo:
    return _get_battery_info("/houses/0/battery/0")

def get_battery_energy_in() -> float:
    battery_info = get_battery_info()

    if battery_info.status == "Charging":
        return battery_info.consumption
    return 0

def get_battery_energy_out() -> float:
    battery_info = get_battery_info()

    if battery_info.status == "Discharging":
        return battery_info.consumption
    return 0

def get_state_of_charge() -> float:
    battery_info = get_battery_info()
    return battery_info.state_of_charge / battery_info.capacity * 100

def get_target_soc() -> Optional[float]:
    battery_info = get_battery_info()
    return battery_info.target_soc / battery_info.capacity * 100 if battery_info.target_soc is not None else None

def set_target_soc(target: Optional[float]) -> None:
    battery_info = get_battery_info()
    if target is not None:
        target = int(target / 100 * battery_info.capacity)
    _set_target_soc("/houses/0/battery/0", target)

def get_battery_status() -> None:
    battery_info = get_battery_info()
    return battery_info.status