#include "Tensor.h"

namespace optmath {

#define INSTANTIATE_TENSOR(typename, alias)                                   \
    template class Tensor<typename>;                                          \
    using alias = Tensor<typename>;

    INSTANTIATE_TENSOR(int8_t, TensorInt8)
    INSTANTIATE_TENSOR(int16_t, TensorInt16);
    INSTANTIATE_TENSOR(int32_t, TensorInt32);
    INSTANTIATE_TENSOR(int64_t, TensorInt64);

    INSTANTIATE_TENSOR(uint8_t, TensorUInt8)
    INSTANTIATE_TENSOR(uint16_t, TensorUInt16);
    INSTANTIATE_TENSOR(uint32_t, TensorUInt32);
    INSTANTIATE_TENSOR(uint64_t, TensorUInt64);

    INSTANTIATE_TENSOR(float, TensorFloat32);
    INSTANTIATE_TENSOR(double, TensorFloat64);

#undef INSTANTIATE_TENSOR

} // namespace optmath
