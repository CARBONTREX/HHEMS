from custom_components.hemsdelft.demkit.thermal import set_target_temp, get_thermal_info


import homeassistant.components.water_heater as water_heater
from homeassistant.components.water_heater import WaterHeaterEntity, WaterHeaterEntityFeature, UnitOfTemperature


class ThermostatSwitchEntity(WaterHeaterEntity):
    _attr_name = "Thermostat"
    _attr_supported_features = WaterHeaterEntityFeature.TARGET_TEMPERATURE
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_target_temperature_high = 0
    _attr_target_temperature_low = 31
    _attr_target_temperature = 23
    _attr_min_temp = 0
    _attr_max_temp = 31
    _attr_current_temperature = 19
    _attr_operation_list = ["auto", "heat", "cool", "off"]
    _attr_current_operation = "auto"
    _attr_state = water_heater.STATE_ON
    _attr_unique_id = "thermostat_switch"


    def update(self):
        thermal_info = get_thermal_info()
        self._attr_current_temperature = thermal_info.current_temperature
        self._attr_target_temperature = thermal_info.target_temperature

    def set_temperature(self, **kwargs):
        temperature = kwargs["temperature"]
        self._attr_target_temperature = temperature
        set_target_temp(temperature)



    def turn_on(self, **kwargs):
        self._attr_state = water_heater.STATE_ON

    def turn_off(self, **kwargs):
        self._attr_state = water_heater.STATE_OFF

    def set_operation_mode(self, operation_mode):
        self._attr_current_operation = operation_mode