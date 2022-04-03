from abc import ABC, abstractmethod

from ..record import RecordBase


class DistanceBase(ABC):
    @abstractmethod
    def __call__(self, first: RecordBase, second: RecordBase) -> float:
        ...
