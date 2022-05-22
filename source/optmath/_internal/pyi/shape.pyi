from typing import List

class Shape:
    def __init__(self, _shape: List[int]) -> None: ...
    def __getitem__(self, index: int) -> int: ...
    def __len__(self) -> int: ...
    def __eq__(self, other: "Shape") -> bool:
        raise TypeError
        ...
    def __ne__(self, other: "Shape") -> bool:
        raise TypeError
        ...