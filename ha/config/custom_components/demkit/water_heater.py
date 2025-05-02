"""Platform for sensor integration."""

from __future__ import annotations
from typing import Final

from homeassistant.components.sensor import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType

from custom_components.hemsdelft.switches.thermostat import ThermostatSwitchEntity

SCAN_INTERVAL: Final = timedelta(seconds=2)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
):
    async_add_entities(
        [
            ThermostatSwitchEntity(),
        ]
    )  # noqa: F821

