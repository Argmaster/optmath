from dataclasses import dataclass
from inspect import isclass
from numbers import Number
from typing import Any, Iterable, Tuple, Type, TypeVar

import numpy as np
from numpy.typing import NDArray

T = TypeVar("T", bound="RecordBase")


@dataclass(frozen=True)
class RecordBase:
    ID: int

    def numeric(self) -> NDArray[np.float64]:
        return np.array(
            [
                self.__dict__[k]
                for k, v in self.__dataclass_fields__.items()
                if isclass(v.type) and issubclass(v.type, Number) and k != "ID"
            ],
            dtype=np.float64,
        )

    @classmethod
    def new(cls: Type[T], data: Iterable[Iterable[Any]]) -> Tuple[T]:
        return tuple(
            cls(index, *(e for e in row)) for index, row in enumerate(data)
        )

    def __len__(self):
        return 1
