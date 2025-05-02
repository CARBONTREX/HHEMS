from .model.measurement import Measurement  # noqa: D100
from .rest import _get_measurement


def get_import() -> Measurement:
    """Retrieve the import measurement from the smart meter.

    Returns:
        Measurement: The import measurement object retrieved from the smart meter

    """
    return _get_measurement("/houses/0/meters/0/import")


def get_export() -> Measurement:
    """Retrieve the export measurement from the smart meter.

    Returns:
        Measurement: The export measurement object retrieved from the smart meter

    """
    return _get_measurement("/houses/0/meters/0/export")
