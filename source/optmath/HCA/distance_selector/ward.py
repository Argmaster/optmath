from typing import List

import numpy as np
from numpy.typing import NDArray

from ..cluster import Cluster
from .selector import DistanceSelectorBase


class Ward(DistanceSelectorBase):
    def new_distance_vector(
        self,
        to_reduce: List[int],
        distance_matrix: NDArray[np.float64],
        new_cluster: Cluster,
        full_cluster_list: List[Cluster],
    ):
        old_size = len(distance_matrix)
        new_vector = []

        for i in range(old_size):
            if i not in to_reduce:
                other_cluster = full_cluster_list[i]
                a = _alpha(new_cluster, other_cluster)
                b = _beta(new_cluster, other_cluster)
                c = _gamma(new_cluster, other_cluster)
                ac_distance, bc_distance = distance_matrix[to_reduce, i]
                distance = (
                    a * ac_distance + b * bc_distance + c * new_cluster.height
                )
                new_vector.append(distance)

        return new_vector


def _alpha(new: Cluster, other: Cluster):
    return (len(new.left) + len(other)) / (
        len(new.left) + len(new.right) + len(other)
    )


def _beta(new: Cluster, other: Cluster):
    return (len(new.right) + len(other)) / (
        len(new.left) + len(new.right) + len(other)
    )


def _gamma(new: Cluster, other: Cluster):
    return (-len(other)) / (len(new.left) + len(new.right) + len(other))
