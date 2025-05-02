from threading import Thread
from hosts.restHost import RestHost
from util.RestApi import RestApi
from util.ComposerStatus import ComposerStatus
from util.entities.EnvEntities import HostEntity
from util.entities.HouseEntities import MeterEntity
from util.entities.ModelRestEntity import ModelRestEntity


class ModelRestComposer:
    def __init__(self, name):
        self.name = name
        self.entities: list[ModelRestEntity] = []

        self.restApi = RestApi(self, 5000, "0.0.0.0")
        self.restApi.start()

        self.host: HostEntity = None
        self.meters: list[MeterEntity] = None
        self.sim_params = None

        self.status: ComposerStatus = ComposerStatus.INACTIVE


    def reset(self):
        self.entities = []
        self.host = None
        self.meters = None
        self.sim_params = None
        self.status = ComposerStatus.INACTIVE
        if self.thread is not None and self.thread.is_alive():
            self.thread.join(timeout=0)
            print("[INF] Thread terminated.")

    def add(self, entity: ModelRestEntity):
        if isinstance(entity, HostEntity):
            self.setHost(entity)
        elif isinstance(entity, MeterEntity):
            self.addMeter(entity)
        else:
            self.entities.append(entity)

    def remove(self, entity_name: str) -> bool:
        for entity in self.entities:
            if entity.name == entity_name:
                self.entities.remove(entity)
                if isinstance(entity, MeterEntity):
                    self.meters.remove(entity)
                elif isinstance(entity, RestHost):
                    self.host = None
                return True
        else:
            print(f"[WRN] Entity {entity_name} not found in the model.")
            return False

    def setHost(self, host: RestHost):
        if self.host is not None:
            print("[WRN] Host already set, replacing with new host.")
            self.entities.remove(self.host)
        self.host = host
        self.entities.append(host)

    def addMeter(self, meter: MeterEntity):
        if self.meters is None:
            self.meters = []
        self.meters.append(meter)
        self.entities.append(meter)

    def load(self):
        print(f"[INF] Starting virtual model composition for {self.name}")

        if self.sim_params is None:
            raise ValueError(
                "Simulation parameters must be set before loading entities"
            )

        if self.host is None:
            raise ValueError("Host must be set before loading entities")

        if self.meters is None:
            self.meters = []
            print("[WRN] No meters defined in the model!")

        for entity in self.entities:
            entity.load(self.host, self.meters, self.sim_params, self.entities)

        self.status = ComposerStatus.LOADED
        print("[INF] Model composition completed.")

    def start(self):
        if self.status == ComposerStatus.ACTIVE:
            print("[WRN] Simulation already started.")
            raise ValueError("Simulation already started.")

        if self.status == ComposerStatus.INACTIVE:
            raise ValueError("Simulation must be loaded before starting.")

        if self.host is None:
            raise ValueError("Host must be set before starting simulation")

        if self.meters is None or len(self.meters) == 0:
            print("[WRN] No meters defined in the model!")

        if self.sim_params is None:
            raise ValueError(
                "Simulation parameters must be set before starting simulation"
            )

        if self.entities is None or len(self.entities) == 0:
            print("[WRN] No entities defined in the model!")

        self.status = ComposerStatus.ACTIVE

        self.host.inner.restApi = True

        self.thread = Thread(target=self._start)
        self.thread.start()

    def _start(self):
        print(f"Starting Simulation.")
        self.host.inner.startSimulation()
