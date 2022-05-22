from io import BytesIO, StringIO
from pathlib import Path

import pytest
from pydantic import ValidationError

from optmath.motifs.fasta import Fasta, InconsistentUsageOfUT

DIR = Path(__file__).parent

SOURCE: str = r"""> Drosophila melanogaster DNA subsequence
atgaccgggatactgataaaaaaaagggggggggcgtacacattagataaacgtatgaagtacgttagactcggcgccgccg
acccctattttttgagcagatttagtgacctggaaaaaaaatttgagtacaaaacttttccgaataaaaaaaaaggggggga
tgagtatccctgggatgacttaaaaaaaagggggggtgctctcccgatttttgaatatgtaggatcattcgccagggtccga
gctgagaattggatgaaaaaaaagggggggtccacgcaatcgcgaaccaacgcggacccaaaggcaagaccgataaaggaga
tcccttttgcggtaatgtgccgggaggctggttacgtagggaagccctaacggacttaataaaaaaaagggggggcttatag
gtcaatcatgttcttgtgaatggatttaaaaaaaaggggggggaccgcttggcgcacccaaattcagtgtgggcgagcgcaa
cggttttggcccttgttagaggcccccgtaaaaaaaagggggggcaattatgagagagctaatctatcgcgtgcgtgttcat
aacttgagttaaaaaaaagggggggctggggcacatacaagaggagtcttccttatcagttaatgctgtatgacactatgta
ttggcccattggctaaaagcccaacttgacaaatggaagatagaatccttgcataaaaaaaagggggggaccgaaagggaag
ctggtgagcaacgacagattcttacgtgcattagctcgcttccggggatctaatagcacgaagcttaaaaaaaaggggggga"""

TITLE: str = r"""Drosophila melanogaster DNA subsequence"""
SEQUENCE: str = r"""ATGACCGGGATACTGATAAAAAAAAGGGGGGGGGCGTACACATTAGATAAACGTATGAAGTACGTTAGACTCGGCGCCGCCGACCCCTATTTTTTGAGCAGATTTAGTGACCTGGAAAAAAAATTTGAGTACAAAACTTTTCCGAATAAAAAAAAAGGGGGGGATGAGTATCCCTGGGATGACTTAAAAAAAAGGGGGGGTGCTCTCCCGATTTTTGAATATGTAGGATCATTCGCCAGGGTCCGAGCTGAGAATTGGATGAAAAAAAAGGGGGGGTCCACGCAATCGCGAACCAACGCGGACCCAAAGGCAAGACCGATAAAGGAGATCCCTTTTGCGGTAATGTGCCGGGAGGCTGGTTACGTAGGGAAGCCCTAACGGACTTAATAAAAAAAAGGGGGGGCTTATAGGTCAATCATGTTCTTGTGAATGGATTTAAAAAAAAGGGGGGGGACCGCTTGGCGCACCCAAATTCAGTGTGGGCGAGCGCAACGGTTTTGGCCCTTGTTAGAGGCCCCCGTAAAAAAAAGGGGGGGCAATTATGAGAGAGCTAATCTATCGCGTGCGTGTTCATAACTTGAGTTAAAAAAAAGGGGGGGCTGGGGCACATACAAGAGGAGTCTTCCTTATCAGTTAATGCTGTATGACACTATGTATTGGCCCATTGGCTAAAAGCCCAACTTGACAAATGGAAGATAGAATCCTTGCATAAAAAAAAGGGGGGGACCGAAAGGGAAGCTGGTGAGCAACGACAGATTCTTACGTGCATTAGCTCGCTTCCGGGGATCTAATAGCACGAAGCTTAAAAAAAAGGGGGGGA"""


class TestFasta:
    def test_load_from_file(self):
        fasta = Fasta.load_from(DIR / "dm.fa")
        assert fasta.title == TITLE
        assert fasta.sequence == SEQUENCE
        fasta.title = "new value"
        with pytest.raises(ValidationError):
            fasta.sequence = "GGGGGGGGGGGGGGGGATTGGC1234567890"
        try:
            fasta.sequence = "GGGGGGGGGGGGGGGGATTGGC1234567890"
        except Exception as e:
            assert (
                str(e)
                == """1 validation error for Fasta
sequence
  Invalid value '1' at location 22: 'TTGGC12345'
                                  ~~~~~~~~^
 (type=value_error.invalidfastaformat)"""
            )

    def test_load_from_file_by_string_path(self):
        fasta = Fasta.load_from(str(DIR / "dm.fa"))
        assert fasta.title == TITLE
        assert fasta.sequence == SEQUENCE

    def test_load_from_string(self):
        fasta = Fasta.load_from(SOURCE)
        assert fasta.title == TITLE
        assert fasta.sequence == SEQUENCE

    def test_load_from_StringIO(self):
        fasta = Fasta.load_from(StringIO(SOURCE))
        assert fasta.title == TITLE
        assert fasta.sequence == SEQUENCE

    def test_load_from_BytesIO(self):
        fasta = Fasta.load_from(BytesIO(SOURCE.encode("utf-8")))
        assert fasta.title == TITLE
        assert fasta.sequence == SEQUENCE

    def test_stringify(self):
        fasta = Fasta.load_from(BytesIO(SOURCE.encode("utf-8")))
        seq = """> Drosophila melanogaster DNA subsequence
ATGACCGGGATACTGATAAAAAAAAGGGGGGGGGCGTACACATTAGATAAACGTATGAAGTACGTTAGACTCGGCGCCGCCG
ACCCCTATTTTTTGAGCAGATTTAGTGACCTGGAAAAAAAATTTGAGTACAAAACTTTTCCGAATAAAAAAAAAGGGGGGGA
TGAGTATCCCTGGGATGACTTAAAAAAAAGGGGGGGTGCTCTCCCGATTTTTGAATATGTAGGATCATTCGCCAGGGTCCGA
GCTGAGAATTGGATGAAAAAAAAGGGGGGGTCCACGCAATCGCGAACCAACGCGGACCCAAAGGCAAGACCGATAAAGGAGA
TCCCTTTTGCGGTAATGTGCCGGGAGGCTGGTTACGTAGGGAAGCCCTAACGGACTTAATAAAAAAAAGGGGGGGCTTATAG
GTCAATCATGTTCTTGTGAATGGATTTAAAAAAAAGGGGGGGGACCGCTTGGCGCACCCAAATTCAGTGTGGGCGAGCGCAA
CGGTTTTGGCCCTTGTTAGAGGCCCCCGTAAAAAAAAGGGGGGGCAATTATGAGAGAGCTAATCTATCGCGTGCGTGTTCAT
AACTTGAGTTAAAAAAAAGGGGGGGCTGGGGCACATACAAGAGGAGTCTTCCTTATCAGTTAATGCTGTATGACACTATGTA
TTGGCCCATTGGCTAAAAGCCCAACTTGACAAATGGAAGATAGAATCCTTGCATAAAAAAAAGGGGGGGACCGAAAGGGAAG
CTGGTGAGCAACGACAGATTCTTACGTGCATTAGCTCGCTTCCGGGGATCTAATAGCACGAAGCTTAAAAAAAAGGGGGGGA"""
        assert f"{fasta:82UT}" == seq

    def test_validate_ut(self):
        with pytest.raises(InconsistentUsageOfUT):
            Fasta(title="", sequence="UT")
