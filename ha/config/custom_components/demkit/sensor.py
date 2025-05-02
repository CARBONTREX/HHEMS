"""Platform for sensor integration."""

from __future__ import annotations
from typing import Final

from homeassistant.components.sensor import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry


from custom_components.hemsdelft.sensors.meter import ExportSensor, ImportSensor
from custom_components.hemsdelft.sensors.battery import (
    BatteryEnergyInSensor,
    BatteryEnergyOutSensor,
)
from custom_components.hemsdelft.sensors.solar import SolarEnergyProductionSensor

SCAN_INTERVAL: Final = timedelta(seconds=2)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    entities = [ImportSensor(), ExportSensor()]
    if entry.data["PV Panels"]:
        entities.append(SolarEnergyProductionSensor())

    if entry.data["Battery"]:
        entities.extend([BatteryEnergyInSensor(), BatteryEnergyOutSensor()])

    async_add_entities(entities)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
):
    async_add_entities(
        [
            ExportSensor(),
            ImportSensor(),
            BatteryEnergyInSensor(),
            BatteryEnergyOutSensor(),
            SolarEnergyProductionSensor(),
        ]
    )  # noqa: F821
