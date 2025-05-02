"""Platform for sensor integration."""

from __future__ import annotations
from typing import Final

from homeassistant.components.sensor import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType

from custom_components.hemsdelft.switches.battery import BatteryTargetSwitch

SCAN_INTERVAL: Final = timedelta(seconds=2)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigType,
    async_add_entities: AddEntitiesCallback,
):
    entities = []
    if entry.data["Battery"]:
        entities.append(BatteryTargetSwitch())

    async_add_entities(entities)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
):
    async_add_entities(
        [
            BatteryTargetSwitch(),
        ]
    )  # noqa: F821
