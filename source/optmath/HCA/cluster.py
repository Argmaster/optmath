from dataclasses import dataclass
from typing import Any, Iterator, List, Tuple, Union

import numpy as np
from numpy.typing import NDArray

from .record import RecordBase

ZMatrixRowT = Tuple[int, int, float, int]

ClusterOrRecord = Union["Cluster", RecordBase]


@dataclass(frozen=True)
class Cluster:
    ID: int
    ob_list: Tuple[ClusterOrRecord, ...]
    height: float = 0.0

    @classmethod
    def new(cls, data: Tuple[Any]) -> List["Cluster"]:
        return [Cluster(record.ID, (record,)) for record in data]

    @property
    def left(self) -> "Cluster":
        assert isinstance(self.ob_list[0], Cluster)
        return self.ob_list[0]

    @property
    def right(self) -> "Cluster":
        assert isinstance(self.ob_list[1], Cluster)
        return self.ob_list[1]

    def __getitem__(self, index: int) -> ClusterOrRecord:
        return self.ob_list[index]

    def __iter__(self) -> Iterator:
        return iter(self.ob_list)

    def __str__(self) -> str:
        return f"Cluster(ID={self.ID},s={len(self)},h={self.height:.3f})"

    def __len__(self) -> int:
        return sum(len(o) for o in self.ob_list)

    def Z(self) -> NDArray[np.float64]:
        offset = len(self)
        z_matrix = [(0, 0, 0.0, 0)] * (self.ID - offset + 1)
        return np.array(
            self._z_matrix(
                z_matrix,
                offset,
            )
        )

    def _z_matrix(
        self, z: List[Tuple[int, int, float, int]], offset: int
    ) -> List[ZMatrixRowT]:
        if not self.left._is_leaf():
            self.left._z_matrix(z, offset)
        if not self.right._is_leaf():
            self.right._z_matrix(z, offset)
        z[self.ID - offset] = self._z_matrix_row()
        return z

    def _is_leaf(self) -> bool:
        return len(self.ob_list) == 1

    def _is_end(self) -> bool:
        return self.left._is_leaf() and self.right._is_leaf()

    def _z_matrix_row(self) -> ZMatrixRowT:
        return (self.left.ID, self.right.ID, self.height, len(self))
