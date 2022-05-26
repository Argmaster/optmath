import json
from pathlib import Path
from typing import List

import pytest

from optmath.motifs.stats import dna_to_int, int_to_dna, score_sequences

DIR = Path(__file__).parent


@pytest.fixture()
def sequences() -> List[str]:
    with (DIR / "exhaustive.json").open("r", encoding="utf-8") as file:
        return json.load(file)


def test_sequence_scoring_simple(sequences: List[str]):
    stats = score_sequences(
        [
            "TCGGGGGTTTTT",
            "CCGGTGACTTAC",
            "ACGGGGATTTTC",
            "TTGGGGACTTTT",
            "AAGGGGACTTCC",
            "TTGGGGACTTCC",
            "TCGGGGATTCAT",
            "TCGGGGATTCCT",
            "TAGGGGAACTAC",
            "TCGGGTATAACC",
        ]
    )
    print(stats.score())
    print(stats.consensus())


def test_sequence_scoring_from_extensive(sequences: List[str]):
    stats = score_sequences(sequences)
    print(stats.score())
    print(stats.consensus())


def test_dna_to_int():
    assert dna_to_int("AG") == 2
    assert dna_to_int("GC") == 9


def test_int_to_dna():
    assert int_to_dna(9, 2) == "GC"
    assert int_to_dna(2, 2) == "AG"
