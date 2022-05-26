import re
from typing import Generator, Iterable, Tuple, TypeVar

from pydantic import BaseModel, validator

from optmath.motifs.distance import hamming_distance


class InvalidSequenceFormat(ValueError):
    pass


class InvalidCharactersInSequence(InvalidSequenceFormat):
    pass


class InconsistentUsageOfUT(InvalidSequenceFormat):
    pass


_SequenceLike = TypeVar("_SequenceLike", bound="SequenceLike")


class SearchResult(BaseModel):
    distance: int
    location: int

    class Config:
        frozen = True


class SequenceLike(BaseModel):

    sequence: str

    class Config:
        validate_all = True
        validate_assignment = True

    @validator("sequence")
    @classmethod
    def sequence_validator(cls, value: str):
        value = value.upper()
        re_match = re.match("^[ATUGC]*(.).*$", value)
        if re_match is None:
            raise InvalidCharactersInSequence(
                "Sequence given is not a valid fasta data."
            )
        else:
            (fail,) = re_match.groups()
            if fail is not None and fail not in "ATUGC":
                message = cls._get_sequence_error_message(value, fail)
                raise InvalidSequenceFormat(message)
        if "U" in value and "T" in value:
            raise InconsistentUsageOfUT(
                "Inconsistent usage of U and T nucleotides in sequence. "
                f"First U at {value.index('U')}, first T at {value.index('T')}"
            )
        return value

    @classmethod
    def _get_sequence_error_message(cls, value: str, fail: str):
        i = value.index(fail)
        left = max(i - 5, 0)
        right = min(i + 5, len(value))
        sub_sequence = value[left:right]
        location_str = str(i)
        return (
            f"Invalid value '{fail}' at location {location_str}: '{sub_sequence}'\n"
            f"{' '*34}~~~{'~'*(i - left + len(location_str) - 2)}^\n"
        )

    def iter_subsequences(
        self,
        length: int,
        move_by: int = 1,
        is_upper: bool = True,
    ) -> Generator[str, None, None]:
        assert move_by <= length
        if not is_upper:
            sequence = self.sequence.lower()
        else:
            sequence = self.sequence
        if len(sequence) < length:
            yield sequence
            return
        for i in range(0, len(sequence) - length + 1, move_by):
            yield sequence[i : i + length]
        return

    def is_dna(self) -> bool:
        return "U" in self.sequence

    def as_rna(self: _SequenceLike) -> _SequenceLike:
        params = self.dict()
        params["sequence"] = self.sequence.replace("T", "U")
        return self.__class__(**params)

    def as_dna(self: _SequenceLike) -> _SequenceLike:
        params = self.dict()
        params["sequence"] = self.sequence.replace("U", "T")
        return self.__class__(**params)

    def format(self, __format_spec: str = "") -> str:  # noqa A003
        return self.__format__(__format_spec)

    def __format__(self, __format_spec: str) -> str:
        line_with, is_upper = self._parse_format(__format_spec)
        body = "\n".join(
            self.iter_subsequences(line_with, line_with, is_upper)
        )
        return body

    def _parse_format(self, __format_spec: str) -> Tuple[int, bool]:
        line_with = 79
        is_upper = True
        if __format_spec:
            re_match = re.match(r"(\d+)([UuLl])?", __format_spec)
            if re_match is not None:
                line_with = int(re_match.group(1))
                is_upper = (
                    re_match.group(2) is None or re_match.group(2) in "Uu"
                )
            else:
                raise ValueError(f"Invalid format string '{__format_spec}'")
        return line_with, is_upper

    def sectors(self, sector_size: int) -> Iterable["SequenceLike"]:
        return tuple(
            SequenceLike(sequence=sub)
            for sub in self.iter_subsequences(sector_size, sector_size)
        )

    def upper(self: _SequenceLike) -> _SequenceLike:
        return self

    def lower(self: _SequenceLike) -> _SequenceLike:
        return self

    def contains(self, item: str, max_distance: int = 0) -> bool:
        # ATTG -> len 4
        # ATTGGGCCCATT
        # ATTG
        #  TTGG
        #   | | -> 2
        #  ATTG
        #   TGGG
        #    ...
        sub_sequences = self.iter_subsequences(len(item))
        if sub_sequences:
            return (
                min(hamming_distance(item, sub) for sub in sub_sequences)
                <= max_distance
            )
        else:
            return False
