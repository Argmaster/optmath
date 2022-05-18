#pragma once

#include "NDBuffer.h"
#include "NDIndex.h"
#include "NDShape.h"
#include <string>
#include <sstream>
#include <iostream>

#define TENSOR_VAL_T __val_T
#define TENSOR_TEMPLATE template <typename TENSOR_VAL_T>

namespace optmath {

    TENSOR_TEMPLATE
    class Tensor {
      private:
        NDBuffer<TENSOR_VAL_T> nd_buffer;

      public:
        Tensor(const NDShape& shape_);
        Tensor();

        const NDShape& shape() const;
        std::ostream&  to_stream(std::ostream& stream) const;
        std::string  to_string() const;

        void Set(const NDIndex& nd_indexer, TENSOR_VAL_T& new_value);
        TENSOR_VAL_T& Get(const NDIndex& nd_indexer);

      public:
        TENSOR_VAL_T* begin();
        TENSOR_VAL_T* end();

        const TENSOR_VAL_T* cbegin() const;
        const TENSOR_VAL_T* cend() const;

        TENSOR_VAL_T& operator[](const NDIndex& index);
        bool          operator==(const Tensor& other) const;

        friend std::ostream& operator<<(std::ostream&               out,
                                        const Tensor<TENSOR_VAL_T>& other) {
            other.nd_buffer.to_stream(out);
            return out;
        }
    };

#define EXTERN_TENSOR(typename, alias)                                        \
    extern template class Tensor<typename>;                                   \
    using alias = Tensor<typename>;

    EXTERN_TENSOR(int8_t, TensorInt8);
    EXTERN_TENSOR(int16_t, TensorInt16);
    EXTERN_TENSOR(int32_t, TensorInt32);
    EXTERN_TENSOR(int64_t, TensorInt64);

    EXTERN_TENSOR(uint8_t, TensorUInt8);
    EXTERN_TENSOR(uint16_t, TensorUInt16);
    EXTERN_TENSOR(uint32_t, TensorUInt32);
    EXTERN_TENSOR(uint64_t, TensorUInt64);

    EXTERN_TENSOR(float, TensorFloat32);
    EXTERN_TENSOR(double, TensorFloat64);

#undef EXTERN_TENSOR

} // namespace optmath

#include "Tensor.tpp"

#undef TENSOR_TEMPLATE
#undef TENSOR_VAL_T
