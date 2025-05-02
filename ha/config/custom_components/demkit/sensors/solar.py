from custom_components.hemsdelft.demkit.solar import get_production

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfPower

class SolarEnergyProductionSensor(SensorEntity):
    _attr_name = "Solar Power Production"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "solar_power_production"

    def update(self) -> None:
        measurement = get_production()
        measurement = round(measurement, 1)
        self._attr_native_value = -measurement
