#pragma once

#include "Tensor.h"

#define TENSOR_METHOD(return_type)                                            \
    TENSOR_TEMPLATE return_type Tensor<TENSOR_VAL_T>::

#define NDBUFFER_T Tensor<TENSOR_VAL_T>

namespace optmath {
    /**
     * @brief Construct a new Tensor object with given shape
     *
     * @param shape_
     */
    TENSOR_METHOD()
    Tensor(const NDShape& shape_)
        : value_buffer(shape_) {
        assert(shape_.size() != 0);
    }
    /**
     * @brief Access shape of tensor
     *
     * @return const NDShape&
     */
    TENSOR_METHOD(const NDShape&) shape() const {
        return this->value_buffer.shape();
    }
    /**
     * @brief Access single element in matrix.
     *
     * @param index_
     * @return TENSOR_VAL_T&
     */
    TENSOR_METHOD(TENSOR_VAL_T&) operator[](const NDIndex& index_) {
        return this->value_buffer[index_];
    }

} // namespace optmath
