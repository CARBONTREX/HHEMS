from custom_components.hemsdelft.demkit.battery import get_battery_energy_in, get_battery_energy_out

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfPower

class BatteryEnergyInSensor(SensorEntity):
    _attr_name = "Battery Power In"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "battery_power_in"

    def update(self) -> None:
        measurement = get_battery_energy_in()
        measurement = round(measurement, 1)
        self._attr_native_value = measurement


class BatteryEnergyOutSensor(SensorEntity):
    _attr_name = "Battery Power Out"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "battery_power_out"

    def update(self) -> None:
        measurement = get_battery_energy_out()
        measurement = round(measurement, 1)
        self._attr_native_value = measurement
