from custom_components.hemsdelft.demkit.model.solar_info import SolarInfo

from .rest import _get_solar_info, _set_solar_state


def get_solar_info() -> SolarInfo:
    return _get_solar_info("/houses/0/solar/0")


def get_production() -> float:
    solar_info = get_solar_info()
    return min(-solar_info.consumption, 0)


def set_solar_state(state: bool) -> None:
    _set_solar_state("/houses/0/solar/0", state)