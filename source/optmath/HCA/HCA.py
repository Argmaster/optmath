from dataclasses import dataclass
from typing import List, Optional

import numpy as np
from numpy.typing import NDArray
from optmath.HCA.cluster import Cluster

from .distance_selector import DistanceSelectorBase


@dataclass
class HCAStep:

    data: List[Cluster]
    distance_selector: DistanceSelectorBase
    distance_matrix: NDArray[np.float64]

    def reduce(self) -> "HCAStep":
        to_reduce, height = self._indexes_to_reduce()
        new_data = []
        reduced_data = []
        for i, row in enumerate(self.data):
            if i in to_reduce:
                reduced_data.append(row)
            else:
                new_data.append(row)

        new_distance_matrix = self.distance_matrix
        if reduced_data:
            new_cluster = Cluster(
                max(c.ID for c in self.data) + 1, tuple(reduced_data), height
            )
            new_data.append(new_cluster)
            new_distance_vector = self.distance_selector.new_distance_vector(
                to_reduce, self.distance_matrix, new_cluster, self.data
            )
            new_distance_matrix = self._new_distance_matrix(
                to_reduce, new_distance_vector
            )

        return HCAStep(
            new_data,
            self.distance_selector,
            new_distance_matrix,
        )

    def _indexes_to_reduce(self):
        min_value = np.inf
        index_pair = []
        for i, row in enumerate(self.distance_matrix):
            for j in range(i):
                if row[j] < min_value:
                    index_pair = (i, j)
                    min_value = row[j]
        return index_pair, min_value

    def _new_distance_matrix(self, to_reduce, new_distance_vector):
        # remove reduced rows and columns
        new_distance_matrix = np.delete(
            np.delete(self.distance_matrix, to_reduce, 0), to_reduce, 1
        )
        if new_distance_vector:
            # add distances for new cluster at the end
            new_distance_matrix = np.vstack(
                (new_distance_matrix, new_distance_vector)
            )
            # add distances for new cluster at the end
            new_distance_matrix = np.hstack(
                (
                    new_distance_matrix,
                    np.reshape(new_distance_vector + [0.0], (-1, 1)),
                )
            )

        return new_distance_matrix

    def __str__(self) -> str:
        return f"Step({', '.join(str(c) for c in self.data)})"


@dataclass
class HCA:

    data: List[Cluster]
    distance_selector: DistanceSelectorBase
    initial_distance_matrix: Optional[NDArray[np.float64]] = None

    def __post_init__(self):
        if self.initial_distance_matrix is None:
            self.initial_distance_matrix = np.array(
                [
                    [
                        self.distance_selector.initial(ob1, ob2)
                        for ob1 in self.data
                    ]
                    for ob2 in self.data
                ]
            )
        self.step = HCAStep(
            self.data,
            self.distance_selector,
            self.initial_distance_matrix,
        )

    def reduce(self) -> HCAStep:
        old_step = self.step
        self.step = old_step.reduce()
        return old_step

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.step.data) == 1:
            raise StopIteration
        else:
            return self.reduce()

    @property
    def last(self) -> HCAStep:
        return self.step

    def result(self) -> Cluster:
        for _ in self:
            pass
        return self.step.data[0]
