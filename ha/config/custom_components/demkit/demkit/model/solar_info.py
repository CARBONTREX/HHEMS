from dataclasses import dataclass  # noqa: D100


@dataclass
class SolarInfo:
    """A class to represent the information of a solar panel.

    Attributes:
        consumption (float): The current consumption of the solar panel in W.

    """

    consumption: float
