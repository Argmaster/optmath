from dataclasses import dataclass
from datetime import datetime
from types import SimpleNamespace

import pytest

from optmath.common.decorators import (
    DeprecatedError,
    deprecated,
    ignore_excess_kwargs,
    statefull,
)


class TestStatefull:
    def test_no_kwargs(self):
        @statefull()
        def no_kwargs(self: SimpleNamespace):
            return 0x33

        assert no_kwargs() == 0x33

    def test_kwargs(self):
        @statefull(a=0x12)
        def kwargs(self: SimpleNamespace):
            assert self.a == 0x12
            return 0x66

        assert kwargs() == 0x66

    def test_kwargs_call_with_params(self):
        @statefull(a=0x12)
        def kwargs_with_params(self: SimpleNamespace, a: int, b: int):
            assert a == 0x55
            assert b == 0x56
            assert self.a == 0x12
            return 0x66

        assert kwargs_with_params(0x55, b=0x56) == 0x66


@ignore_excess_kwargs
@dataclass
class A:
    a: int
    b: int


class TestIgnoreExcessKwargs:
    def test_no_excess(self):

        instance = A(0x33, 0x44)
        assert instance.a == 0x33
        assert instance.b == 0x44

    def test_with_excess_args(self):

        instance = A(0x33, 0x44, 0x22)
        assert instance.a == 0x33
        assert instance.b == 0x44

    def test_with_excess_kwargs(self):

        instance = A(0x33, 0x44, c=0x22)
        assert instance.a == 0x33
        assert instance.b == 0x44

    def test_with_excess_mixed(self):

        instance = A(0x33, 0x44, 0x11, c=0x22)
        assert instance.a == 0x33
        assert instance.b == 0x44


class TestDeprecated:
    def test_simple_mark(self):
        @deprecated()
        def function():
            pass

        with pytest.warns(FutureWarning):
            function()

    def test_date_bomb_no_explode(self):
        @deprecated(date_bomb=datetime(4000, 1, 1, 0, 0, 0, 0))
        def function():
            pass

        with pytest.warns(FutureWarning):
            function()

    def test_date_bomb_explode(self):
        @deprecated(date_bomb=datetime(1990, 1, 1, 0, 0, 0, 0))
        def function():  # pragma: no cover
            pass

        with pytest.raises(DeprecatedError):
            function()

    def test_version_bomb_no_explode(self):
        @deprecated(version_bomb="4000.0.0")
        def function():
            pass

        with pytest.warns(FutureWarning):
            function()

    def test_version_bomb_explode(self):
        @deprecated(version_bomb="0.0.0")
        def function():  # pragma: no cover
            pass

        with pytest.raises(DeprecatedError):
            function()
