# distutils: language = c++
# cython: language_level=3

from .ndindex cimport NDIndex
from .ndshape cimport NDShape
from .tensor cimport Tensor as CppTensorImpl

from numbers import Number
from typing import Any, List, Optional, Tuple, Union

from optmath._internal.shape import Shape


def shape_of(
    array: List[Number] | Tuple[Number] | List[Any] | Tuple[Any],
    initial: Optional[List[int]] = None,
) -> List[int]:
    if initial is None:
        initial = []
    initial.append(len(array))
    for sub in array:
        if isinstance(sub, (list, tuple)):
            shape_of(sub, initial)
    return initial


cdef class _TensorI32:
    cdef CppTensorImpl[int] _c_tensor

    def __cinit__(self, __init: List | Tuple, shape: Optional[List[int] | Tuple[int]] = None):
        if shape is None:
            dest_shape = shape_of(__init)
        else:
            dest_shape = shape
        self._c_tensor = Tensor[int](NDShape(dest_shape))
        self._initialize_c_tensor(__init)

    def _initialize_c_tensor(
        self,
        initializer: List | Tuple,
        index: Union[Tuple[()], Tuple[int, ...]] = (),
    ):
        for i, value in enumerate(initializer):
            dest_index = (*index, i)
            if isinstance(value, (tuple, list)):
                self._initialize_c_tensor(value, dest_index)
            else:
                if len(dest_index) < self._c_tensor.shape().size():
                    raise IndexError(
                        "Initializer has invalid shape of %d dimensions, required %d" % (
                            len(dest_index), self._c_tensor.shape().size())
                    )
                self._c_tensor.Set(NDIndex(dest_index), value)

    def __str__(self) -> str:
        return self._c_tensor.to_string().decode("utf-8")
