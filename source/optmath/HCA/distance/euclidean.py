from typing import cast

import numpy as np

from ..record import RecordBase
from .distance import DistanceBase


class Euclidean(DistanceBase):
    def __call__(self, first: RecordBase, second: RecordBase) -> float:
        return cast(
            float, np.sqrt(np.sum((first.numeric() - second.numeric()) ** 2))
        )
