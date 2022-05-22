from typing import Generator, Set


def exhaustive(sequence: str, k: int, d: int) -> Set[str]:
    for k_mer in k_mer_iterator(sequence, k):
        for pattern in d_mismatches_iterator(k_mer, d):
            print(pattern)


def k_mer_iterator(sequence: str, k: int) -> Generator[str, None, None]:
    yield ""


def d_mismatches_iterator(k_mer: str, d: int) -> Generator[str, None, None]:
    yield ""
