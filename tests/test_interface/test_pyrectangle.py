import pytest
from optmath._internal.interface import PyRectangle


class TestPyRectangle:
    @pytest.fixture()
    def set_up(self):
        return PyRectangle(0, 1, 2, 3)

    def test_attribs(self, set_up: PyRectangle):
        rectangle = set_up
        assert rectangle.x0 == 0
        assert rectangle.y0 == 1
        assert rectangle.x1 == 2
        assert rectangle.y1 == 3
