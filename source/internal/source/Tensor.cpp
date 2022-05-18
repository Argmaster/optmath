#include "Tensor.h"

namespace optmath {

#define INSTANTIATE_TENSOR(typename) template class Tensor<typename>;

    INSTANTIATE_TENSOR(int8_t)
    INSTANTIATE_TENSOR(int16_t);
    INSTANTIATE_TENSOR(int32_t);
    INSTANTIATE_TENSOR(int64_t);

    INSTANTIATE_TENSOR(uint8_t)
    INSTANTIATE_TENSOR(uint16_t);
    INSTANTIATE_TENSOR(uint32_t);
    INSTANTIATE_TENSOR(uint64_t);

    INSTANTIATE_TENSOR(float);
    INSTANTIATE_TENSOR(double);

#undef INSTANTIATE_TENSOR

} // namespace optmath
