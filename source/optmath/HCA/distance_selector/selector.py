from dataclasses import dataclass
from typing import List, Tuple, cast

import numpy as np
from numpy.typing import NDArray

from optmath.HCA.record import RecordBase

from ..cluster import Cluster
from ..distance import DistanceBase


@dataclass(frozen=True)
class DistanceSelectorBase:
    distance: DistanceBase

    def initial(self, first: Cluster, second: Cluster) -> float:
        return self.distance(
            cast(RecordBase, first[0]), cast(RecordBase, second[0])
        )

    def new_distance_vector(
        self,
        to_reduce: Tuple[int, int],
        distance_matrix: NDArray[np.float64],
        new_cluster: Cluster,
        old_data: List[Cluster],
    ) -> NDArray[np.float64]:
        raise NotImplementedError()
