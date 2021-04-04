import abc
import enum
from typing import Any


class SwaVanMockTask(abc.ABC):

    @property
    def id(self) -> Any:
        return "NOT_IMPLEMENTED"

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass


class ServerTypes(enum.Enum):
    REST = 1
