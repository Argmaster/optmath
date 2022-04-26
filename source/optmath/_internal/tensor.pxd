from libcpp cimport bool

from .ndindex cimport NDIndex
from .ndshape cimport NDShape


cdef extern from "Tensor.h" namespace "optmath":
    cdef cppclass Tensor[TENSOR_VAL_T]:
        Tensor(const NDShape&)
        Tensor()
        const NDShape& shape() const
        TENSOR_VAL_T* begin()
        TENSOR_VAL_T* end()

        const TENSOR_VAL_T* cbegin() const
        const TENSOR_VAL_T* cend() const

        TENSOR_VAL_T&  operator[](const NDIndex& index)
        bool           operator==(const Tensor& other) const
