from dataclasses import dataclass  # noqa: D100
from enum import Enum
from typing import Optional


class BatteryStatus(Enum):
    """Enum representing the status of a battery.

    Attributes:
        CHARGING (str): The battery is currently charging.
        DISCHARGING (str): The battery is currently discharging.
        IDLE (str): The battery is idle and not charging or discharging.
        ERROR (str): There is an error with the battery.

    """

    CHARGING = 0
    DISCHARGING = 1
    IDLE = 2
    ERROR = -1


@dataclass
class BatteryInfo:
    """A class to represent the information of a battery.

    Attributes:
        capacity (float): The total capacity of the battery in Wh.
        max_charge (float): The maximum charge rate of the battery in W.
        max_discharge (float): The maximum discharge rate of the battery in W.
        state_of_charge (float): The current state of charge of the battery as a percentage (0-100%).
        status (BatteryStatus): The current status of the battery.
        consumption (float): The current consumption of the battery in W.

    """

    capacity: float
    max_charge: float
    max_discharge: float
    state_of_charge: float
    target_soc: Optional[float]
    status: BatteryStatus
    consumption: float
