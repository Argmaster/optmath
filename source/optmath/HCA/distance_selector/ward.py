from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray

from ..cluster import Cluster
from .selector import DistanceSelectorBase


class Ward(DistanceSelectorBase):
    def new_distance_vector(
        self,
        to_reduce: Tuple[int, int],
        distance_matrix: NDArray[np.float64],
        new_cluster: Cluster,
        full_cluster_list: List[Cluster],
    ) -> NDArray[np.float64]:
        old_size = len(distance_matrix)
        new_vector = []

        for i in range(old_size):
            if i not in to_reduce:
                other_cluster = full_cluster_list[i]
                total_item_count = (
                    len(new_cluster.left)
                    + len(new_cluster.right)
                    + len(other_cluster)
                )
                a = _alpha(new_cluster, other_cluster, total_item_count)
                b = _beta(new_cluster, other_cluster, total_item_count)
                c = _gamma(other_cluster, total_item_count)
                ac_distance, bc_distance = distance_matrix[to_reduce, i]
                distance = (
                    a * ac_distance + b * bc_distance + c * new_cluster.height
                )
                new_vector.append(distance)

        return np.array(new_vector)


def _alpha(new: Cluster, other: Cluster, total_item_count: int) -> float:
    return (len(new.left) + len(other)) / (total_item_count)


def _beta(new: Cluster, other: Cluster, total_item_count: int) -> float:
    return (len(new.right) + len(other)) / (total_item_count)


def _gamma(other: Cluster, total_item_count: int) -> float:
    return (-len(other)) / (total_item_count)
