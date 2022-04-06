from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import numpy as np
from numpy.typing import NDArray

from ..cluster import Cluster
from ..distance import DistanceBase


@dataclass(frozen=True)
class DistanceSelectorBase(ABC):
    distance: DistanceBase

    def initial(self, first: Cluster, second: Cluster) -> float:
        return self.distance(first[0], second[0])

    @abstractmethod
    def new_distance_vector(
        self,
        to_reduce: List[int],
        distance_matrix: NDArray[np.float64],
        new_cluster: Cluster,
        old_data: List[Cluster],
    ) -> NDArray[np.float64]:
        ...
