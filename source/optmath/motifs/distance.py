from typing import Sequence


def humming_distance(first: Sequence, second: Sequence) -> int:
    return sum(f != s for f, s in zip(first, second))