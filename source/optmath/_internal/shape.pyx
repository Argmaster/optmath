# distutils: language = c++
# cython: language_level=3

from libcpp.vector cimport vector

from .ndshape cimport NDShape


cdef class Shape:
    cdef NDShape _shape

    def __cinit__(self, shape_: list | tuple):
        self._shape = NDShape(shape_)

    def __getitem__(self, index: int):
        max_index = self._shape.size()
        if index >= max_index or index < 0:
            raise IndexError(
                f"Index out of bounds: got {index}, max {max_index}, min 0")
        return self._shape.get(index)

    def __len__(self):
        return self._shape.size()

    def __eq__(self, other: Shape):
        return self._shape == other._shape

    def __ne__(self, other: Shape):
        return self._shape != other._shape

    # def __iter__(self):
    #     return self._shape.begin()

# cdef extern from "Tensor.h" namespace "optmath":
#     cdef cppclass Tensor[__val_T]:
#         Tensor(const NDShape&)
#         const NDShape& shape()
#
#
# cdef class TensorI32:
#     cdef Tensor[int] *_tensor
#
#     def __cinit__(self):
#         self._tesnor = new Tensor[int]()
#
#     def __dealloc__(self):
#         del self._tensor
