from dataclasses import dataclass  # noqa: D100


@dataclass
class Measurement:
    """A class to represent a measurement with a value and a unit.

    Attributes:
    ----------
    value : float
        The numerical value of the measurement.
    unit : str
        The unit of the measurement

    """

    value: float
    unit: str
