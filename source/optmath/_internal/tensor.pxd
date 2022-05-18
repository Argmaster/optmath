from libcpp cimport bool
from libcpp.string cimport string

from .ndindex cimport NDIndex
from .ndshape cimport NDShape


cdef extern from "Tensor.h" namespace "optmath":
    cdef cppclass Tensor[TENSOR_VAL_T]:
        Tensor(const NDShape&)
        Tensor()
        const NDShape& shape() const
        string to_string() const

        void Set(const NDIndex& nd_indexer, TENSOR_VAL_T& new_value);
        TENSOR_VAL_T& Get(const NDIndex& nd_indexer);

        TENSOR_VAL_T* begin()
        TENSOR_VAL_T* end()

        const TENSOR_VAL_T* cbegin() const
        const TENSOR_VAL_T* cend() const

        TENSOR_VAL_T&  operator[](const NDIndex& index)
        bool           operator==(const Tensor& other) const
