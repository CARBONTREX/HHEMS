from custom_components.hemsdelft.demkit.battery import set_target_soc, get_state_of_charge, get_target_soc, get_battery_status


from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.components.number import NumberDeviceClass, NumberEntity
from homeassistant.components.humidifier import HumidifierEntity, HumidifierDeviceClass, HumidifierAction, MODE_AUTO, HumidifierEntityFeature


class BatteryTargetSwitch(HumidifierEntity):
    _attr_name = "Battery Manual Targeting Mode"
    _attr_device_class = HumidifierDeviceClass.HUMIDIFIER
    _attr_native_unit_of_measurement = "%"
    _attr_action = "Idle"
    _attr_is_on = False
    _attr_current_humidity = 50
    _attr_target_humidity = None
    _attr_unique_id = "battery_target_switch"

    def update(self):
        current_soc = get_state_of_charge()
        # round current_soc to 2 digits behind the comma
        current_soc = round(current_soc, 2)
        self._attr_current_humidity = current_soc
        self._attr_target_humidity = get_target_soc()
        self._attr_action = get_battery_status()

    def set_humidity(self, humidity):
        set_target_soc(humidity)
        self._attr_target_humidity = humidity

    def turn_on(self, **kwargs):
        self._attr_is_on = True
        self._attr_target_humidity = 50
        set_target_soc(50)
        self._attr_action = "On"
        self.update()

    def turn_off(self, **kwargs):
        self._attr_is_on = False
        self._attr_target_humidity = None
        set_target_soc(None)
        self._attr_action = "Auto"
        self.update()