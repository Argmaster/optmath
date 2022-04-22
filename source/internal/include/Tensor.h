#pragma once

#include "NDBuffer.h"
#include "NDIndex.h"
#include "NDShape.h"

#define TENSOR_VAL_T __val_T
#define TENSOR_TEMPLATE template <typename TENSOR_VAL_T>

namespace optmath {

    TENSOR_TEMPLATE
    class Tensor : private NDBuffer<TENSOR_VAL_T> {
      public:
        Tensor(const NDShape& shape_);

        using NDBuffer<TENSOR_VAL_T>::shape;
        using NDBuffer<TENSOR_VAL_T>::operator[];
    };

#define EXTERN_TENSOR(typename) extern template class Tensor<typename>;

    EXTERN_TENSOR(int8_t);
    EXTERN_TENSOR(int16_t);
    EXTERN_TENSOR(int32_t);
    EXTERN_TENSOR(int64_t);

    EXTERN_TENSOR(uint8_t);
    EXTERN_TENSOR(uint16_t);
    EXTERN_TENSOR(uint32_t);
    EXTERN_TENSOR(uint64_t);

    EXTERN_TENSOR(float);
    EXTERN_TENSOR(double);

#undef EXTERN_TENSOR

} // namespace optmath

#include "Tensor.tpp"

#undef TENSOR_TEMPLATE
#undef TENSOR_VAL_T
