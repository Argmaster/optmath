#include "NDBuffer.h"

namespace optmath {

#define INSTANTIATE_NDBUFFER(typename) template class NDBuffer<typename>;

    INSTANTIATE_NDBUFFER(int8_t);
    INSTANTIATE_NDBUFFER(int16_t);
    INSTANTIATE_NDBUFFER(int32_t);
    INSTANTIATE_NDBUFFER(int64_t);

    INSTANTIATE_NDBUFFER(uint8_t)
    INSTANTIATE_NDBUFFER(uint16_t);
    INSTANTIATE_NDBUFFER(uint32_t);
    INSTANTIATE_NDBUFFER(uint64_t);

    INSTANTIATE_NDBUFFER(float);
    INSTANTIATE_NDBUFFER(double);

#undef INSTANTIATE_NDBUFFER

} // namespace optmath
