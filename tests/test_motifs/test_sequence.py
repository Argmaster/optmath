import pytest

from optmath.motifs.sequence import SequenceLike

DNA_SEQ_1: str = "ATTTGGGCCCAA"
DNA_SEQ_2: str = "AUUUGGGCCCAA"


class TestSequenceLike:
    @pytest.fixture()
    def dna_seq_1(self) -> SequenceLike:
        return SequenceLike(sequence=DNA_SEQ_1)

    @pytest.fixture()
    def dna_seq_2(self) -> SequenceLike:
        return SequenceLike(sequence=DNA_SEQ_2)

    def test_simple_creation(self, dna_seq_1: SequenceLike):
        assert DNA_SEQ_1 == dna_seq_1.sequence

    def test_is_dna(self, dna_seq_2: SequenceLike):
        assert dna_seq_2.is_dna() is True

    def test_format(self, dna_seq_2: SequenceLike):
        assert f"{dna_seq_2:80U}" == DNA_SEQ_2
