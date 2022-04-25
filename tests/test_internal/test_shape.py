import pytest

from optmath._internal import Shape


def test_3D_shape():
    shape = Shape([1, 2, 3])
    assert shape is not None


def test_3D_shape_from_tuple():
    shape = Shape((1, 2, 3))
    assert shape is not None


def test_shape_index_access():
    shape = Shape([1, 2, 3])
    assert shape[0] == 1
    assert shape[1] == 2
    assert shape[2] == 3
    with pytest.raises(IndexError):
        shape[3]


def test_shape_index_access_tuple():
    shape = Shape((1, 2, 3))
    assert shape[0] == 1
    assert shape[1] == 2
    assert shape[2] == 3
    with pytest.raises(IndexError):
        shape[3]


def test_shape_dimension_count():
    shape = Shape([3, 5, 1])
    assert len(shape) == 3
    shape = Shape([3, 1])
    assert len(shape) == 2
    shape = Shape([3, 1, 6, 3, 756, 342])
    assert len(shape) == 6


def test_shape_equality():
    first = Shape([3, 5, 1])
    second = Shape([4, 9])
    third = Shape([3, 5, 1])
    assert (first == first) is True
    assert (first == second) is False
    assert (first == third) is True
    with pytest.raises(TypeError):
        assert first == 54


def test_shape_inequality():
    first = Shape([3, 5, 1])
    second = Shape([4, 9])
    third = Shape([3, 5, 1])
    assert (first != first) is False
    assert (first != second) is True
    assert (first != third) is False
    with pytest.raises(TypeError):
        assert first != 54
