from custom_components.hemsdelft.demkit.model.thermal_info import ThermalInfo

from .rest import _get_thermal_info, _set_target_temp


def get_thermal_info() -> ThermalInfo:
    return _get_thermal_info("/houses/0/thermal/0")

def set_target_temp(temp: float) -> None:
    _set_target_temp("/houses/0/thermal/0", temp)