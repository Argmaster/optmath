import pytest

from optmath._internal import Index


def test_3D_index():
    index = Index([1, 2, 3])
    assert index is not None


def test_3D_index_from_tuple():
    index = Index((1, 2, 3))
    assert index is not None


def test_index_index_access():
    index = Index([1, 2, 3])
    assert index[0] == 1
    assert index[1] == 2
    assert index[2] == 3
    with pytest.raises(IndexError):
        index[3]


def test_index_index_access_tuple():
    index = Index((1, 2, 3))
    assert index[0] == 1
    assert index[1] == 2
    assert index[2] == 3
    with pytest.raises(IndexError):
        index[3]


def test_index_dimension_count():
    index = Index([3, 5, 1])
    assert len(index) == 3
    index = Index([3, 1])
    assert len(index) == 2
    index = Index([3, 1, 6, 3, 756, 342])
    assert len(index) == 6


def test_index_equality():
    first = Index([3, 5, 1])
    second = Index([4, 9])
    third = Index([3, 5, 1])
    assert (first == first) is True
    assert (first == second) is False
    assert (first == third) is True
    with pytest.raises(TypeError):
        assert first == 54


def test_index_inequality():
    first = Index([3, 5, 1])
    second = Index([4, 9])
    third = Index([3, 5, 1])
    assert (first != first) is False
    assert (first != second) is True
    assert (first != third) is False
    with pytest.raises(TypeError):
        assert first != 54
