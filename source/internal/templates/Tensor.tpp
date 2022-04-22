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
        : NDBuffer<TENSOR_VAL_T>(shape_) {
        assert(shape_.size() != 0);
        assert(this->begin() != nullptr);
    }

} // namespace optmath
