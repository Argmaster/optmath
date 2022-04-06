from dataclasses import dataclass
from typing import Any, List, Tuple, Union

import numpy as np
from numpy.typing import NDArray

from .record import RecordBase

ZMatrixRowT = Tuple[int, int, float, int]


@dataclass(frozen=True)
class Cluster:
    ID: int
    ob_list: Tuple[Union["Cluster", RecordBase], ...]
    height: int = 0

    @classmethod
    def new(cls, data: Tuple[Any]) -> List["Cluster"]:
        return [Cluster(record.ID, (record,)) for record in data]

    def __iter__(self):
        return iter(self.ob_list)

    def __str__(self) -> str:
        return f"Cluster(ID={self.ID},s={len(self)},h={self.height:.3f})"

    def __len__(self) -> int:
        return sum(len(o) for o in self.ob_list)

    def Z(self) -> NDArray[np.float64]:
        return np.array(self._z_matrix())

    def _z_matrix(self) -> List[ZMatrixRowT]:
        z = []
        for sub in self.ob_list:
            assert isinstance(sub, Cluster)
            self._z_sub_cluster(z, sub)

        z.append(self._z_matrix_row())
        return z

    def _z_sub_cluster(self, z: List[ZMatrixRowT], sub: "Cluster"):
        if isinstance(sub, Cluster) and not sub._is_leaf():
            if sub._is_end():
                z.append(sub._z_matrix_row())
            else:
                z.extend(sub._z_matrix())

    def _is_leaf(self) -> bool:
        return len(self.ob_list) == 1

    def _is_end(self) -> bool:
        return all(o._is_leaf() for o in self.ob_list)

    def _z_matrix_row(self) -> ZMatrixRowT:
        return (self.ob_list[0].ID, self.ob_list[1].ID, self.height, len(self))
