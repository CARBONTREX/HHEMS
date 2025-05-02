"""Config flow for Hello World integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries
from .demkit.sim import sim
from typing import Any

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required("PV Panels", default=False): bool,
    vol.Required("Battery", default=False): bool,
    vol.Required("Dishwasher", default=False): bool,
    vol.Required("Washing Machine", default=False): bool,
})


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""

        self.knownLoads: list[sim.KnownLoad] = []
        self.unknownLoads: list[sim.UnknownLoad] = []

        self.knownLoadsSchema = {}
        self.unknownLoadsSchema = {}

        self.simDevicesUserInput: dict[str, Any] = {}

        self.simDevices: sim.SimDevices = sim.SimDevices(
            False, False, False, False)

        self.simKnownLoads: list[sim.KnownLoad] = []
        self.simUnknownLoads: list[sim.UnknownLoad] = []

        self.errors = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:

            self.simDevicesUserInput = user_input

            self._get_real_devices()

            return await self.async_step_knownLoads()

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, description_placeholders={
                "form_description": "Virtual Devices"
            }
        )

    async def async_step_knownLoads(self, user_input=None):
        """Handle known loads."""
        if user_input is not None:

            for load in self.knownLoads:
                if user_input[load.name]:
                    self.simKnownLoads.append(load)

            return await self.async_step_unknownLoads()

        return self.async_show_form(
            step_id="knownLoads", data_schema=vol.Schema(self.knownLoadsSchema), description_placeholders={
                "form_description": "Loads"
            })

    async def async_step_unknownLoads(self, user_input=None):
        """Handle unknown loads."""
        if user_input is not None:

            for load in self.unknownLoads:
                if user_input[load.name] > 0:
                    self.simUnknownLoads.append(
                        sim.UnknownLoad(entity_id=load.entity_id, name=load.name, consumption=user_input[load.name]))


            self.simDevices.battery = self.simDevicesUserInput["Battery"]
            self.simDevices.pv = self.simDevicesUserInput["PV Panels"]
            self.simDevices.dishwasher = self.simDevicesUserInput["Dishwasher"]
            self.simDevices.washingmachine = self.simDevicesUserInput["Washing Machine"]

            _LOGGER.info(self.simDevices, self.simKnownLoads,
                         self.simUnknownLoads)

            simStarted = sim.startSim(self.simDevices, self.simKnownLoads, self.simUnknownLoads)

            if not simStarted:
                self.errors["base"] = "Unexpected error starting simulation"
                return

            return self.async_create_entry(
                title="DEMKit Integration", data=self.simDevicesUserInput
            )

        return self.async_show_form(
            step_id="unknownLoads", data_schema=vol.Schema(self.unknownLoadsSchema), description_placeholders={
                "form_description": "Loads"
            }, errors=self.errors)

    def _get_real_devices(self):
        entities = self.hass.states._states_data
        for entity in entities.values():
            if entity.entity_id.startswith("light."):
                self.unknownLoads.append(sim.UnknownLoad(
                    entity_id=entity.entity_id, name=entity.name, consumption=0))
            elif "device_class" in entity.attributes:
                if entity.attributes["device_class"] == "power":
                    self.knownLoads.append(sim.KnownLoad(
                        entity_id=entity.entity_id, name=entity.name))

        for load in self.knownLoads:
            self.knownLoadsSchema[vol.Required(
                load.name, default=False)] = bool

        for load in self.unknownLoads:
            self.unknownLoadsSchema[vol.Optional(load.name, default=0)] = int
