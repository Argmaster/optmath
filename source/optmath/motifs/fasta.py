import re
from contextlib import suppress
from io import BytesIO, StringIO
from pathlib import Path
from typing import Iterator, Tuple, Union

from .sequence import SequenceLike


class Fasta(SequenceLike):
    """Class encapsulating block of Fasta sequence data.

    >>> fasta = Fasta(title="Some Sequence", sequence="ATGACCGGGATACTGATAAAAAAAAGGGGGGGGGCGTACACATTAGATAAACGTATGAAGTACGTTAGACTCGGCGCCGCCG")
    >>> fasta
    > Some Sequence
    ATGACCGGGATACTGATAAAAAAAAGGGGGGGGGCGTACACATTAGATAAACGTATGAAGTACGTTAGACTCGGCGCCGC
    CG
    >>> print(fasta.format("15U"))
    ATGACCGGGATACTG
    ATAAAAAAAAGGGGG
    GGGGCGTACACATTA
    GATAAACGTATGAAG
    TACGTTAGACTCGGC
    GCCGCCG

    Parameters
    ----------
    title : str
        Fasta file title
    sequence : str
        DNA/RNA sequence

    Raises
    ------
    InvalidCharactersInSequence
        raised for invalid character in sequence, only 'A','T','U','C','G','a','t','u','c','g' allowed.
    InvalidFastaFormat
        raised for invalid fasta format, when content cannot be parsed.
    InconsistentUsageOfUT
        raised for sequence using bot U and T nucleotides.
    """

    title: str

    @classmethod
    def load_from(
        cls,
        source: Union[str, bytes, Path, StringIO, BytesIO],
        encoding: str = "utf-8",
    ):
        if isinstance(source, Path):
            source_str = Path(source).read_text(encoding=encoding)
        elif isinstance(source, StringIO):
            source.seek(0)
            source_str = source.read()
        elif isinstance(source, BytesIO):
            source.seek(0)
            source_str = source.read().decode(encoding=encoding)
        elif isinstance(source, str):
            source_str = cls._load_from_str(source, encoding)
        elif isinstance(source, bytes):
            source_str = source.decode("utf-8")
        else:
            raise TypeError(
                "Invalid source type, expected one of str, bytes, "
                f"Path, StringIO, BytesIO, got {type(source)}"
            )

        title, sequence = cls._parse_fasta(source_str)
        return cls(
            title=title, sequence=sequence.replace("\n", "").strip().upper()
        )

    @classmethod
    def _load_from_str(cls, source, encoding):
        with suppress(OSError):
            source_path = Path(source)
            if source_path.exists():
                return source_path.read_text(encoding=encoding)
        return source

    @classmethod
    def _parse_fasta(cls, source: str) -> Tuple[str, str]:
        re_match = re.match(r">\s*(.*?)\n(.*)\s*", source, re.DOTALL)
        if re_match is None:
            raise ValueError("File is not a valid fasta file.")
        return re_match.groups()

    def __str__(self) -> str:
        return self.sequence

    def __iter__(self) -> Iterator[str]:
        return iter(self.sequence)

    def __repr__(self) -> str:
        return f"{self:80UT}"

    def format(self, __format_spec: str = "") -> str:  # noqa A003
        return self.__format__(__format_spec)

    def __format__(self, __format_spec: str) -> str:
        line_with, is_upper, use_title = self._parse_format(__format_spec)
        body = "\n".join(
            self.iter_subsequences(line_with, line_with, is_upper)
        )
        if use_title is True:
            return f"> {self.title}\n{body}"
        else:
            return body

    def _parse_format(self, __format_spec: str) -> Tuple[int, bool, bool]:
        line_with = 79
        is_upper = True
        use_title = False
        if __format_spec:
            re_match = re.match(r"(\d+)([UuLl])?([Tt])?", __format_spec)
            if re_match is not None:
                line_with = int(re_match.group(1))
                is_upper = (
                    re_match.group(2) is None or re_match.group(2) in "Uu"
                )
                use_title = re_match.group(3) is not None
            else:
                raise ValueError(f"Invalid format string '{__format_spec}'")
        return line_with, is_upper, use_title


if __name__ == "__main__":
    import doctest

    doctest.testmod()
