from typing import Self
from ctrl.thermal.thermostat import Thermostat
from dev.bufDev import BufDev
from dev.curtDev import CurtDev
from dev.electricity.solarPanelDev import SolarPanelDev
from dev.meterDev import MeterDev
from dev.thermal.combinedHeatPowerDev import CombinedHeatPowerDev
from dev.thermal.dhwDev import DhwDev
from dev.thermal.gasBoilerDev import GasBoilerDev
from dev.thermal.heatPumpDev import HeatPumpDev
from dev.thermal.thermalBufConvDev import ThermalBufConvDev
from dev.thermal.zoneDev2R2C import ZoneDev2R2C
from dev.tsDev import TsDev
from util.Complex import RustComplex
from util.entities.ModelRestEntity import ModelRestEntity
from util.entities.EnvEntities import (
    HostEntity,
    SunEntity,
    WeatherEntity,
)


class MeterEntity(ModelRestEntity):
    def __init__(
        self, name, commodities: list[str] = None, weights: dict[str, float] = None
    ):
        super().__init__(name)
        self.inner: MeterDev = None

        if not commodities or not weights:
            self.commodities = ["ELECTRICITY"]
            self.weights = {"ELECTRICITY": 1}
        else:
            self.commodities = commodities
            self.weights = weights

    def load(
        self,
        host: HostEntity,
        meters: list[Self],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        super().load()

        self.inner = MeterDev(self.name, host.inner, list(self.commodities))

class CurtEntity(ModelRestEntity):
    def __init__(
        self,
        name: str,
        filename: str,
        filenameReactive: str,
        column: int,
        timeBase: int,
    ):
        super().__init__(name)
        self.filename = filename
        self.filenameReactive = filenameReactive
        self.column = column
        self.timeBase = timeBase

    def load(
        self,
        host: HostEntity,
        meters: list[MeterEntity],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        super().load()
        unc = CurtDev(self.name, host.inner)
        unc.filename = self.filename
        unc.filenameReactive = self.filenameReactive
        unc.column = params.get("houseNum", 0)
        unc.timeBase = self.timeBase
        unc.strictComfort = not params.get("useIslanding", False)

        for entity in meters:
            if "ELECTRICITY" in entity.commodities:
                entity.inner.addDevice(unc)
                break
        else:
            raise ValueError("No meter found with ELECTRICITY commodity")


import util.alpg as alpg


class SolarPanelEntity(ModelRestEntity):
    def __init__(self, name: str):
        super().__init__(name)

    def load(
        self,
        host: HostEntity,
        meters: list[MeterEntity],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        super().load()
        idx = alpg.indexFromFile(
            params.get("photoVoltaicSettings"), params.get("houseNum", 0)
        )
        # in one line try to find the SunEntity in entities and assign it to sun
        sun = next(
            (entity.inner for entity in entities if isinstance(entity, SunEntity)), None
        )

        pv = SolarPanelDev(self.name, host.inner, sun)
        pv_specs = alpg.listFromFile(params.get("photoVoltaicSettings"))

        pv.size = pv_specs[idx][3]  # in m2, (12 panels of 1.6 m2)
        pv.efficiency = pv_specs[idx][2]  # efficiency in percent
        pv.azimuth = pv_specs[idx][1]  # in degrees, 0=north, 90 is east
        pv.inclination = pv_specs[idx][0]  # angle

        pv.strictComfort = not params.get("useIslanding", False)

        sm = next(
            (
                entity
                for entity in entities
                if isinstance(entity, MeterEntity)
                and "ELECTRICITY" in entity.commodities
            ),
            None,
        )

        if sm is None:
            raise ValueError("No meter found with ELECTRICITY commodity")
        pv.commodities = sm.commodities
        sm.inner.addDevice(pv)


class TimeShiftableEntity(ModelRestEntity):
    def __init__(
        self,
        name: str,
        profile: list[list[float]] = None,
        timeBase: int = 60,
    ):
        super().__init__(name)

        if profile is None:
            raise ValueError("profile cannot be None")

        self.profile: list[complex] = [complex(item[0], item[1]) for item in profile]
        self.timeBase = timeBase

    def load(
        self,
        host: HostEntity,
        meters: list[MeterEntity],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        super().load()
        ts = TsDev(self.name, host.inner)

        ts.profile = self.profile
        ts.timeBase = self.timeBase
        ts.strictComfort = not params.get("useIslanding", False)

        for entity in meters:
            if "ELECTRICITY" in entity.commodities:
                entity.inner.addDevice(ts)
                break
        else:
            raise ValueError("No meter found with ELECTRICITY commodity")


class BatteryEntity(ModelRestEntity):
    def __init__(
        self,
        name: str,
    ):
        super().__init__(name)

    def load(
        self,
        host: HostEntity,
        meters: list[MeterEntity],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        super().load()
        idx = alpg.indexFromFile(
            params.get("batterySettings"), params.get("houseNum", 0)
        )
        sm = next(
            (
                entity
                for entity in entities
                if isinstance(entity, MeterEntity)
                and "ELECTRICITY" in entity.commodities
            ),
            None,
        )

        buf = BufDev(self.name, host.inner, sm)
        bat_specs = alpg.listFromFile(params.get("batterySettings"))

        buf.chargingPowers = [-1 * bat_specs[idx][0], bat_specs[idx][0]]
        buf.capacity = bat_specs[idx][1]
        buf.initialSoC = bat_specs[idx][2]

        buf.soc = buf.initialSoC

        sm = next(
            (
                entity
                for entity in entities
                if isinstance(entity, MeterEntity)
                and "ELECTRICITY" in entity.commodities
            ),
            None,
        )
        buf.commodities = sm.commodities
        buf.discrete = False

        # Marks to spawn events
        buf.highMark = buf.capacity * 0.8
        buf.lowMark = buf.capacity * 0.2

        buf.strictComfort = not params.get("useIslanding", False)

        sm.inner.addDevice(buf)

        if params.get("useFillMethod"):
            buf.meter = sm.inner


class ZoneEntity(ModelRestEntity):
    def __init__(
        self,
        name: str,
        rFloor: float = 0.001,
        rEnvelope: float = 0.0064,
        cFloor: float = 5100 * 3600,
        cZone: float = 21100 * 3600,
        initialTemperature: float = 18.5,
    ):
        super().__init__(name)
        self.inner: ZoneDev2R2C = None
        self.rFloor = rFloor
        self.rEnvelope = rEnvelope
        self.cFloor = cFloor
        self.cZone = cZone
        self.initialTemperature = initialTemperature

    def load(
        self,
        host: HostEntity,
        meters: list[MeterEntity],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        super().load()
        sm = next(
            (
                entity
                for entity in entities
                if isinstance(entity, MeterEntity)
                and "ELECTRICITY" in entity.commodities
            ),
            None,
        )
        if sm is None:
            raise ValueError("No meter found with HEATING commodity")

        weather = next(
            (entity.inner for entity in entities if isinstance(entity, WeatherEntity)),
            None,
        )

        sun = next(
            (entity.inner for entity in entities if isinstance(entity, SunEntity)), None
        )

        zone = ZoneDev2R2C(self.name, weather, sun, host.inner)

        zone.perfectPredictions = params.get("usePP", True)
        zone.rFloor = self.rFloor  # K/W
        zone.rEnvelope = self.rEnvelope  # K/W
        zone.cFloor = self.cFloor  # J/K
        zone.cZone = self.cZone  # J/K
        zone.initialTemperature = self.initialTemperature  # C

        zone.gainFile = params.get("gainFile")
        zone.ventilationFile = params.get("ventilationFile")
        zone.gainColumn = params.get("houseNum", 0)
        zone.ventilationColumn = params.get("houseNum", 0)

        zone.addWindow(10, 180)
        self.inner = zone


class ThermostatEntity(ModelRestEntity):
    def __init__(
        self,
        name: str,
        temperatureSetpointHeating: float = 21.0,
        temperatureSetpointCooling: float = 23.0,
        temperatureMin: float = 21.0,
        temperatureMax: float = 23.0,
        temperatureDeadband: list[float] = [-0.1, 0.0, 0.5, 0.6],
        preheatingTime: float = 3600,
    ):
        super().__init__(name)
        self.inner: Thermostat = None
        self.temperatureSetpointHeating = temperatureSetpointHeating
        self.temperatureSetpointCooling = temperatureSetpointCooling
        self.temperatureMin = temperatureMin
        self.temperatureMax = temperatureMax
        self.temperatureDeadband = temperatureDeadband
        self.preheatingTime = preheatingTime

    def load(
        self,
        host: HostEntity,
        meters: list[MeterEntity],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        super().load()
        zone = next(
            (entity.inner for entity in entities if isinstance(entity, ZoneEntity)),
            None,
        )
        if zone is None:
            raise ValueError("No zone found")

        thermostat = Thermostat(self.name, zone, None, host.inner)
        thermostat.temperatureSetpointHeating = self.temperatureSetpointHeating
        thermostat.temperatureSetpointCooling = self.temperatureSetpointCooling
        thermostat.temperatureMin = self.temperatureMin
        thermostat.temperatureMax = self.temperatureMax
        thermostat.temperatureDeadband = self.temperatureDeadband
        thermostat.preheatingTime = self.preheatingTime
        thermostat.perfectPredictions = params.get("usePP", True)
        thermostat.timeBase = params.get("ctrlTimeBase", 900)

        idx = alpg.indexFromFile(
            params.get("thermostatStartTimes"), params.get("houseNum", 0)
        )

        therm_starttimes = alpg.listFromFile(params.get("thermostatStartTimes"))
        therm_setpoints = alpg.listFromFile(params.get("thermostatSetpoints"))

        for j in range(0, len(therm_setpoints[idx])):
            thermostat.addJob(therm_starttimes[idx][j], therm_setpoints[idx][j])

        self.inner = thermostat


class DhwEntity(ModelRestEntity):
    def __init__(
        self,
        name: str,
    ):
        super().__init__(name)
        self.inner: DhwDev = None

    def load(
        self,
        host: HostEntity,
        meters: list[MeterEntity],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        super().load()

        dhw = DhwDev(self.name, host.inner)
        dhwFile = params.get("dhwFile")
        if dhwFile is None:
            raise ValueError("dhwFile cannot be None")
        dhw.dhwFile = dhwFile
        dhw.dhwColumn = params.get("houseNum", 0)
        dhw.perfectPredictions = params.get("usePP", True)

        self.inner = dhw


class HeatSourceEntity(ModelRestEntity):
    def __init__(
        self,
        name: str,
    ):
        super().__init__(name)
        self.inner: ThermalBufConvDev = None

    def load(
        self,
        host: HostEntity,
        meters: list[MeterEntity],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        super().load()
        heat_specs = alpg.listFromFileStr(params.get("heatingSettings"))

        if heat_specs[-1][0] == "CONVENTIONAL":  # Gas boiler
            heatsource = GasBoilerDev(self.name, host.inner)
            heatsource.producingTemperatures = [0, 60.0]
        elif heat_specs[-1][0] == "HP":
            heatsource = HeatPumpDev(self.name, host.inner)
            heatsource.producingTemperatures = [0, 35.0]
            heatsource.producingPowers = [
                0,
                4500,
            ]  # use [-4500, 4500] for cooling, but this is unsupported yet
            heatsource.commodities = ["ELECTRICITY", "HEAT"]
            heatsource.cop = {
                "ELECTRICITY": 4.0
            }  # Pretty common CoP, each unit of electricity consumed produces 4 units of heat
        else:
            heatsource = CombinedHeatPowerDev(self.name, host.inner)
            heatsource.commodities = ["ELECTRICITY", "NATGAS", "HEAT"]  # INPUT, OUTPUT
            heatsource.cop = {"ELECTRICITY": (-13.5 / 6.0), "NATGAS": (13.5 / 21.0)}

        heatsource.capacity = 50000.0
        heatsource.soc = 25000.0
        heatsource.initialSoC = 25000.0
        heatsource.strictComfort = not params.get("useIslanding", False)
        heatsource.islanding = params.get("useIslanding", False)

        self.inner = heatsource

        zone = next(
            (entity.inner for entity in entities if isinstance(entity, ZoneEntity)),
            None,
        )
        if zone is None:
            raise ValueError("No zone found")

        thermostat = next(
            (
                entity.inner
                for entity in entities
                if isinstance(entity, ThermostatEntity)
            ),
            None,
        )
        if thermostat is None:
            raise ValueError("No thermostat found")

        heatsource.addZone(zone)
        heatsource.addThermostat(thermostat)

        sm = next(
            (
                entity.inner
                for entity in entities
                if isinstance(entity, MeterEntity) and "ELECTRICITY" in entity.commodities
            ),
            None,
        )
        if sm is None:
            raise ValueError("No meter found with ELECTRICITY commodity")

        gm = next(
            (
                entity.inner
                for entity in entities
                if isinstance(entity, MeterEntity) and "NATGAS" in entity.commodities
            ),
            None,
        )
        if gm is None:
            raise ValueError("No meter found with NATGAS commodity")

        sm.addDevice(heatsource)
        gm.addDevice(heatsource)


class HeatPumpEntity(ModelRestEntity):
    def __init__(
        self,
        name: str,
        producingTemperatures: list[float] = [0.0, 35.0],
        producingPowers: list[float] = [-4500, 4500],
    ):
        super().__init__(name)
        self.producingTemperatures = producingTemperatures
        self.producingPowers = producingPowers

    def load(
        self,
        host: HostEntity,
        meters: list[MeterEntity],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        super().load()

        heat_specs = alpg.listFromFileStr(params.get("heatingSettings"))
        heatsource = next(
            (entity for entity in entities if isinstance(entity, HeatSourceEntity)),
            None,
        )

        dhw = next(
            (entity.inner for entity in entities if isinstance(entity, DhwEntity)), None
        )

        if not heat_specs[-1][0] == "HP":
            heatsource.inner.addDhwTap(dhw)
        else:
            # Heatpump has not enough power to provide tapwater, so we need another to heat water. Note that the generic heatsource is not applicable to planning
            dhwsrc = HeatPumpDev(self.name, host.inner)
            dhwsrc.producingTemperatures = self.producingTemperatures
            dhwsrc.producingPowers = self.producingPowers
            dhwsrc.perfectPredictions = params.get("usePP", True)
            dhwsrc.strictComfort = not params.get("useIslanding", False)
            dhwsrc.islanding = params.get("useIslanding", False)
            dhwsrc.commodities = ["ELECTRICITY", "HEAT"]
            dhwsrc.cop = {
                "ELECTRICITY": 4.0
            }  # Pretty common CoP, each unit of electricity consumed produces 4 units of heat
            dhwsrc.addDhwTap(dhw)

            sm = next(
                (
                    entity.inner
                    for entity in entities
                    if isinstance(entity, MeterEntity)
                    and "ELECTRICITY" in entity.commodities
                ),
                None,
            )
            if sm is None:
                raise ValueError("No meter found with ELECTRICITY commodity")

            gm = next(
                (
                    entity.inner
                    for entity in entities
                    if isinstance(entity, MeterEntity) and "NATGAS" in entity.commodities
                ),
                None,
            )
            if gm is None:
                raise ValueError("No meter found with NATGAS commodity")

            sm.addDevice(dhwsrc)
            gm.addDevice(dhwsrc)
