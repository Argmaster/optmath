#pragma once

#include "NDBuffer.h"
#include "NDShape.h"
#include "NDIndex.h"

#define TENSOR_VAL_T __val_T
#define TENSOR_TEMPLATE template <typename TENSOR_VAL_T>

namespace optmath {

    TENSOR_TEMPLATE
    class Tensor {

      private:
        NDBuffer<TENSOR_VAL_T> value_buffer;

      public:
        Tensor(const NDShape& shape_);

        const NDShape& shape() const;
        TENSOR_VAL_T& operator[](const NDIndex&);

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
