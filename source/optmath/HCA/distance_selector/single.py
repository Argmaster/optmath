from typing import List

import numpy as np
from numpy.typing import NDArray

from ..cluster import Cluster
from .selector import DistanceSelectorBase


class SingleLinkage(DistanceSelectorBase):
    def new_distance_vector(
        self,
        to_reduce: List[int],
        distance_matrix: NDArray[np.float64],
        _: Cluster,
        __: List[Cluster],
    ):
        old_size = len(distance_matrix)
        return [
            min(distance_matrix[to_reduce, i])
            for i in range(old_size)
            if i not in to_reduce
        ]
