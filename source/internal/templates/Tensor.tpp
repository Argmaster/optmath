#pragma once

#include "Tensor.h"

#define TENSOR_METHOD(return_type)                                            \
    TENSOR_TEMPLATE return_type Tensor<TENSOR_VAL_TYPE>::

#define TENSOR_T Tensor<TENSOR_VAL_TYPE>

namespace optmath {
    TENSOR_METHOD()
    Tensor(const NDShape& shape_)
        : value_buffer(shape_) {
            assert(shape_.size() != 0);
        }

} // namespace optmath
