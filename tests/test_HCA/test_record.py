from dataclasses import dataclass
from typing import ClassVar

from optmath.HCA.record import RecordBase


@dataclass(frozen=True)
class ExampleRecord(RecordBase):
    attr: int
    attr2: float
    attr3: str
    attr4: ClassVar[str] = "sth"


def test_record_numeric():
    ob = ExampleRecord(0, 1, 3.14, "name")
    assert len(ob.numeric()) == 2
