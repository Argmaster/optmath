import numpy as np

from ..record import RecordBase
from .distance import DistanceBase


class Chebyshev(DistanceBase):
    def __call__(self, first: RecordBase, second: RecordBase) -> float:
        return np.max(first.numeric() - second.numeric())
