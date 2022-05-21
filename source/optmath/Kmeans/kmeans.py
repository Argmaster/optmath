from dataclasses import dataclass
from inspect import isclass
from typing import Callable, Optional, Tuple, Type, TypeVar, Union

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy.typing import NDArray
from rich.progress import Progress

from optmath import RecordBase
from optmath.HCA.distance import DistanceBase, Euclidean

GroupedT = Tuple[Tuple[RecordBase, ...]]
EndConditionFuncT = Callable[[GroupedT, GroupedT], bool]


def Kmeans(
    autoscaled_data: Tuple[RecordBase, ...],
    cluster_count: Optional[int] = None,
    iter_limit: int = 50,
    distance: Union[DistanceBase, Type[DistanceBase]] = Euclidean,
    active_end_condition: Optional[EndConditionFuncT] = None,
) -> "KmeansResultView":

    if isclass(distance):
        distance = distance()

    assert iter_limit > 0
    assert len(autoscaled_data) > 0
    record_class = autoscaled_data[0].__class__

    if cluster_count is None:
        cluster_count = int(np.ceil(np.log(np.sqrt(len(autoscaled_data)))))

    centers = _random_sample(autoscaled_data, cluster_count)
    groups: Optional[GroupedT] = None

    with Progress() as progress:
        task = progress.add_task("Clustering...", total=iter_limit)
        _iteration_index = 0

        for _iteration_index in range(iter_limit):
            distance_matrix = _get_distances_matrix(
                autoscaled_data, distance, centers
            )
            # matrix format
            # __________| pc1   | pc2   | ...
            # object 1  |       |       |
            new_clusters = _get_new_clusters(
                autoscaled_data, centers, distance_matrix
            )
            # check optional end condition.
            if (
                groups is not None
                and active_end_condition is not None
                and active_end_condition(groups, new_clusters)
            ):
                break

            new_centers = _get_new_centers(
                autoscaled_data, record_class, new_clusters
            )

            centers = new_centers
            groups = new_clusters
            progress.update(task, advance=1)
        progress.update(
            task,
            total=iter_limit,
            description=f"Finished after {_iteration_index} iterations.",
        )

    return KmeansResultView(groups)


def _get_new_centers(
    autoscaled_data: Tuple[RecordBase, ...],
    record_class: Type[RecordBase],
    new_clusters: Tuple[Tuple[RecordBase, ...]],
) -> Tuple[RecordBase, ...]:
    new_centers = []
    for cluster_index, cluster in enumerate(new_clusters):
        numeric_obs = np.array([ob.numeric() for ob in cluster])
        new_center = record_class(
            len(autoscaled_data) + cluster_index,
            *np.mean(numeric_obs, axis=0),
        )
        new_centers.append(new_center)
    return tuple(new_centers)


def _get_new_clusters(
    autoscaled_data: Tuple[RecordBase, ...],
    centers: Tuple[RecordBase, ...],
    distance_matrix: NDArray[np.float64],
) -> Tuple[Tuple[RecordBase, ...]]:
    return tuple(
        tuple(
            ob
            for ob, min_id in zip(
                autoscaled_data,
                np.argmin(distance_matrix, axis=1),
            )
            if min_id == group_id
        )
        for group_id, _ in enumerate(centers)
    )


def _get_distances_matrix(
    autoscaled_data: Tuple[RecordBase, ...],
    distance: DistanceBase,
    centers: Tuple[RecordBase, ...],
) -> NDArray[np.float64]:
    return np.array(
        [
            [distance(ob, center) for center in centers]
            for ob in autoscaled_data
        ]
    )


_T = TypeVar("_T")


def _random_sample(data: Tuple[_T], cluster_count: int) -> Tuple[_T, ...]:
    rand_index = np.random.uniform(0, len(data), cluster_count)
    return tuple(data[np.int64(index)] for index in rand_index)


@dataclass
class KmeansResultView:

    clusters: Tuple[Tuple[RecordBase, ...]]

    def plot_cluster(self):
        ax = Axes3D(plt.figure(figsize=(10, 10)))
        ax.scatter()
