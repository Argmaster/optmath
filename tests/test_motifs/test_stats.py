import json
from pathlib import Path
from typing import List

import pytest

from optmath.motifs.stats import score_sequences

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
