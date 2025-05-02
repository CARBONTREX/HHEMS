

from abc import ABC, abstractmethod
from typing import Self

# from util.entities.HouseEntities import MeterEntity
# from util.entities.EnvEntities import HostEntity

class ModelRestEntity(ABC):
	def __init__(self, name: str):
		self.name: str = name

	@abstractmethod
	def load(self, host = None, meters = None, simparams: dict[str, any] = None, entities: list[Self] = None):
		print(f"Loading entity: {self.name}")