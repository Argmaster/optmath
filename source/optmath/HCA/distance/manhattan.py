from typing import cast

import numpy as np

from ..record import RecordBase
from .distance import DistanceBase


class Manhattan(DistanceBase):
    def __call__(self, first: RecordBase, second: RecordBase) -> float:
        return cast(float, np.sum(np.abs(first.numeric() - second.numeric())))
