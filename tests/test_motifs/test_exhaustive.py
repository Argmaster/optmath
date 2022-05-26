import json
from pathlib import Path

import pytest

from optmath.motifs.distance import hamming_distance
from optmath.motifs.exhaustive import exhaustive, neighbors, print_mismatches
from optmath.motifs.fasta import Fasta

DIR = Path(__file__).parent


@pytest.fixture()
def dna() -> Fasta:
    return Fasta.load_from(DIR / "dm.fa")


@pytest.fixture()
def dna2() -> Fasta:
    return Fasta.load_from(DIR / "dm2.fa")


@pytest.mark.skip("Too time consuming to include in standard test cycle.")
def test_exhaustive(dna: Fasta):
    assert len(exhaustive(dna, 15, 4, 82)) == 104870


@pytest.mark.skip("Too time consuming to include in standard test cycle.")
def test_exhaustive_2(dna2: Fasta):
    seq = exhaustive(dna2, 15, 4, 82)
    with (DIR / "exhaustive2.json").open("w", encoding="utf-8") as file:
        json.dump(list(seq), file)


@pytest.mark.parametrize(
    ("sequence", "distance", "expected_size"),
    [
        ("AT", 2, 16),
        ("ATGAAACT", 2, 277),
        ("ATGAAACT", 4, 7459),
        ("ATGAAACGTTCCT", 2, 742),
        ("ATGAAACGTTCCT", 5, 379120),
    ],
)
def test_mismatches(sequence: str, distance: int, expected_size: int):
    seq = neighbors(sequence, distance)
    for sub_pattern in seq:
        assert hamming_distance(sub_pattern, sequence) <= distance
    assert len(seq) == expected_size


def test_mismatch_print():
    print_mismatches("AAATAGGT", "AGTTAAGT")
