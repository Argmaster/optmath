from typing import cast

import numpy as np

from ..record import RecordBase
from .distance import DistanceBase


class Chebyshev(DistanceBase):
    def __call__(self, first: RecordBase, second: RecordBase) -> float:
        return cast(float, np.max(np.abs(first.numeric() - second.numeric())))
