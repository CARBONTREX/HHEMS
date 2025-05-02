from dataclasses import dataclass  # noqa: D100


@dataclass
class ThermalInfo:
    """A class to represent the information of a thermostat.

    Attributes:
        current_temperature (float): The current temperature in °C.
        target_temperature (float): The target temperature in °C.
        heating_power (float): The current heating power in W.
        consumption (float): The current consumption of the heating in W.

    """

    current_temperature: float
    target_temperature: float
    heating_power: float
    consumption: float
