from typing import Self

from pytz import timezone
from environment.sunEnv import SunEnv
from environment.weatherEnv import WeatherEnv
from hosts.restHost import RestHost
from util.entities.ModelRestEntity import ModelRestEntity
# from util.entities.HouseEntities import MeterEntity

class MeterEntity(ModelRestEntity):
    pass

class HostEntity(ModelRestEntity):
    def __init__(self, name: str):
        super().__init__(name)
        self.inner = RestHost()

    def load(
        self,
        host: Self,
        meters: list[MeterEntity],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        super().load()
        if params is None:
            raise ValueError("params cannot be None for HostEntity")

        self.inner.timeBase = params.get("timeBase")
        self.inner.timeDelayBase = params.get("timeDelayBase")
        self.inner.timeOffset = params.get("timeOffset")
        self.inner.timezone = timezone(params.get("timeZone"))
        self.inner.intervals = params.get("intervals")
        self.inner.startTime = params.get("startTime")
        self.inner.db.database = params.get("database")
        self.inner.db.prefix = params.get("dataPrefix")
        self.inner.extendedLogging = params.get("extendedLogging")
        self.inner.logDevices = params.get("logDevices", True)
        self.inner.logFlow = params.get("logFlow", False)
        self.inner.enablePersistence = params.get("enablePersistence")

        if params.get("clearDB"):
            self.inner.clearDatabase()

    def start(self):
        self.inner.startSimulation()


class WeatherEntity(ModelRestEntity):
    def __init__(self, name: str):
        super().__init__(name)
        self.inner: WeatherEnv = None

    def load(
        self,
        host: HostEntity,
        meters: list[MeterEntity],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        self.inner = WeatherEnv(self.name, host.inner)
        self.inner.weatherFile = params.get("weatherFile")


class SunEntity(ModelRestEntity):
    def __init__(self, name: str):
        super().__init__(name)
        self.inner: SunEnv = None

    def load(
        self,
        host: HostEntity,
        meters: list[MeterEntity],
        params: dict[str, any],
        entities: list[ModelRestEntity],
    ):
        self.inner = SunEnv(self.name, host.inner)
        self.inner.irradianceFile = params.get("irradianceFile")
