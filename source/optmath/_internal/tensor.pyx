# distutils: language = c++
# cython: language_level=3

from .ndshape cimport NDShape
from .tensor cimport Tensor as CppTensorImpl


cdef class _TensorI32:
    cdef CppTensorImpl[int] _tensor;

    def __cinit__(self, shape_: list | tuple):
        self._tensor = Tensor[int](NDShape(shape_))
