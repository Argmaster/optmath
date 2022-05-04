import re
from dataclasses import dataclass
from inspect import isclass
from numbers import Number
from typing import Any, Iterable, List, Tuple, Type, TypeVar

import numpy as np
from numpy.typing import NDArray

T = TypeVar("T", bound="RecordBase")


_CAMEL_CASE_REGEX: re.Pattern = re.compile(r"([A-Z0-9][a-z0-9]+)")


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
    def new(cls: Type[T], data: Iterable[Iterable[Any]]) -> Tuple[T, ...]:
        return tuple(
            cls(index, *(e for e in row)) for index, row in enumerate(data)
        )

    @classmethod
    def class_name(cls):
        return " ".join(_CAMEL_CASE_REGEX.findall(cls.__qualname__)).lower()

    def __len__(self):
        return 1

    def columns(self) -> List[str]:
        return [k for k, _ in self.__dataclass_fields__.items()]


def autoscale(data: NDArray[np.float64]) -> NDArray[np.float64]:
    return np.array(
        [(column - column.mean()) / column.std() for column in data.T]
    ).T


def to_numpy_array(data: Tuple[RecordBase]) -> NDArray[np.float64]:
    return np.array(
        [d.numeric() for d in data],
        dtype=np.float64,
    )
