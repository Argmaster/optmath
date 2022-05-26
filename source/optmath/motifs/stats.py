from collections import Counter
from typing import Any
from typing import Counter as CounterT
from typing import List, Sequence

from pydantic import BaseModel

_NUCLEOTIDES: str = "ATGC"


class SequenceStats(BaseModel):
    stats: List[CounterT[str]]

    def score(self) -> int:
        return sum(
            sum(column.values()) - column.most_common()[0][1]
            for column in self.stats
        )

    def consensus(self) -> str:
        sequence = []
        for column in self.stats:
            nucleotide, _ = column.most_common()[0]
            sequence.append(nucleotide)
        return "".join(sequence)


def score_sequences(motifs: Sequence[str]) -> SequenceStats:
    length = len(motifs[0])
    assert _items_have_same_length(motifs, length)
    columns: List[CounterT[str]] = [Counter() for _ in range(length)]
    for motif in motifs:
        for column_index, symbol in enumerate(motif):
            counter = columns[column_index]
            for nucleotide in _NUCLEOTIDES:
                counter[nucleotide] = counter.get(nucleotide, 0) + (
                    symbol == nucleotide
                )
    assert columns is not None
    return SequenceStats(stats=columns)


def _items_have_same_length(sequence: Sequence[Any], length: int) -> bool:
    return all(len(item) == length for item in sequence)


_MAP = {
    "A": 0,
    0: "A",
    "C": 1,
    1: "C",
    "G": 2,
    2: "G",
    "T": 3,
    3: "T",
}
_BASE = 4


def dna_to_int(value: str) -> int:
    multiplier = 1
    total = 0
    for val in reversed(value):
        total += _MAP[val] * multiplier
        multiplier *= _BASE
    return total


def int_to_dna(value: int, size: int) -> str:
    seq = []
    while value:
        reminder = value % _BASE
        value //= _BASE
        print(reminder, _MAP[reminder], value)
        seq.append(_MAP[reminder])
    seq.reverse()
    return f'{"".join(seq):A>{size}}'
