from numbers import Number
from typing import List, Optional, Tuple, Union

RecursiveIntInitializer = Union[int, List["RecursiveIntInitializer"]]
RecursiveNumberInitializer = Union[Number, List["RecursiveNumberInitializer"]]

def shape_of(__sequence: RecursiveNumberInitializer) -> List[int]: ...

class Tensor:
    def __init__(
        self,
        __init: List[RecursiveNumberInitializer],
        shape: Optional[List[int] | Tuple[int]] = None,
    ) -> None: ...
    def __str__(self) -> str: ...

class _TensorI32:
    def __init__(
        self,
        __init: List[RecursiveIntInitializer],
        shape: Optional[List[int] | Tuple[int]] = None,
    ) -> None: ...
    def __str__(self) -> str: ...
