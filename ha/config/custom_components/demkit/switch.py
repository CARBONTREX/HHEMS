"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry


from custom_components.hemsdelft.switches.solar import PvPanelSwitch

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    entities = []
    if entry.data["PV Panels"]:
        entities.append(PvPanelSwitch())
    async_add_entities(entities)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    async_setup_entry,
    discovery_info=None,
):
    async_add_entities(
        [
            PvPanelSwitch(),
        ]
    )  # noqa: F821
