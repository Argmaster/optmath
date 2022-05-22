from pathlib import Path

import pytest

from optmath.motifs.fasta import Fasta

DIR = Path(__file__).parent


@pytest.fixture()
def dna() -> Fasta:
    return Fasta.load_from(DIR / "dm.fa")


def test_exhaustive(dna: Fasta):
    print(dna.format())
