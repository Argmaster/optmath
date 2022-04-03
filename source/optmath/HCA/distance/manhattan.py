import numpy as np

from ..record import RecordBase
from .distance import DistanceBase


class Manhattan(DistanceBase):
    def __call__(self, first: RecordBase, second: RecordBase) -> float:
        return np.sum(first.numeric() - second.numeric())
