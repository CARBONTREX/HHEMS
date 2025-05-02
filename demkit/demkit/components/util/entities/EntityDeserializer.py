from dataclasses import dataclass
from typing import TypedDict

from util.entities.EnvEntities import (
    HostEntity,
    SunEntity,
    WeatherEntity,
)
from util.entities.HouseEntities import (
    BatteryEntity,
    CurtEntity,
    DhwEntity,
    HeatPumpEntity,
    HeatSourceEntity,
    MeterEntity,
    SolarPanelEntity,
    ThermostatEntity,
    TimeShiftableEntity,
    ZoneEntity,
)
from util.entities.ModelRestEntity import ModelRestEntity


entity_types: dict[str, ModelRestEntity] = {
    "host": HostEntity,
    "weather": WeatherEntity,
    "sun": SunEntity,
    "meter": MeterEntity,
    "curt": CurtEntity,
    "solar_panel": SolarPanelEntity,
    "timeshiftable": TimeShiftableEntity,
    "battery": BatteryEntity,
    "zone": ZoneEntity,
    "thermostat": ThermostatEntity,
    "dhw": DhwEntity,
    "heat_source": HeatSourceEntity,
    "heat_pump": HeatPumpEntity,
}


class EntityParams(TypedDict):
    name: str


@dataclass
class GenericEntity:
    type: str = None
    entity_params: EntityParams = None

    # create a from class method to create an instance from a dictionary
    @classmethod
    def from_dict(cls, data: dict):
        # check if data contains all required keys
        if "type" not in data:
            raise ValueError("Entity type is missing")

        if "entity" not in data:
            raise ValueError("Entity params is missing")

        return cls(type=data.get("type"), entity_params=data.get("entity"))


def deserialize(data) -> ModelRestEntity:
    generic_entity = GenericEntity.from_dict(data)

    entity_type = generic_entity.type.lower()
    entity_class = entity_types.get(entity_type)

    if entity_class is None:
        raise ValueError(f"Unknown entity type: {entity_type}")

    entity_params: EntityParams = generic_entity.entity_params
    entity: ModelRestEntity = entity_class(**entity_params)

    return entity
