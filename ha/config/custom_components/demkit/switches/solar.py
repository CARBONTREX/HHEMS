from custom_components.hemsdelft.demkit.solar import set_solar_state

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity


class PvPanelSwitch(SwitchEntity):
    _attr_name = "PV Panel"
    _attr_assumed_state = True
    _attr_device_class = SwitchDeviceClass.OUTLET
    _attr_unique_id = "pv_panel_switch"


    def turn_on(self, **kwargs) -> None:
        print("Turning on")
        self.is_on = True
        set_solar_state(True)

    def turn_off(self, **kwargs) -> None:
        print("Turning off")
        self.is_on = False
        set_solar_state(False)
