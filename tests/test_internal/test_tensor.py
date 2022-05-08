from optmath._internal import _TensorI32


def test_tensor_i32_impl_given_shape_1D():
    tensor = _TensorI32([1, 3, 5], shape=[3])
    assert str(tensor) == "[1, 3, 5]"


def test_tensor_i32_impl_deduce_shape_1D():
    tensor = _TensorI32([1, 3, 5])
    assert str(tensor) == "[1, 3, 5]"
