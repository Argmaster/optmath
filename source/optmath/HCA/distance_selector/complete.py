from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray

from ..cluster import Cluster
from .selector import DistanceSelectorBase


class CompleteLinkage(DistanceSelectorBase):
    def new_distance_vector(
        self,
        to_reduce: Tuple[int, int],
        distance_matrix: NDArray[np.float64],
        _: Cluster,
        __: List[Cluster],
    ) -> NDArray[np.float64]:
        old_size = len(distance_matrix)
        return np.array(
            [
                max(distance_matrix[to_reduce, i])
                for i in range(old_size)
                if i not in to_reduce
            ]
        )
