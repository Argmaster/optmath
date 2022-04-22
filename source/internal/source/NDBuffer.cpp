#include "NDBuffer.h"

namespace optmath {

#define INSTANTIATE_NDBUFFER(typename, alias)                                 \
    template class NDBuffer<typename>;                                        \
    using alias = NDBuffer<typename>;

    INSTANTIATE_NDBUFFER(int8_t, NDBufferInt8);
    INSTANTIATE_NDBUFFER(int16_t, NDBufferInt16);
    INSTANTIATE_NDBUFFER(int32_t, NDBufferInt32);
    INSTANTIATE_NDBUFFER(int64_t, NDBufferInt64);

    INSTANTIATE_NDBUFFER(uint8_t, NDBufferUInt8)
    INSTANTIATE_NDBUFFER(uint16_t, NDBufferUInt16);
    INSTANTIATE_NDBUFFER(uint32_t, NDBufferUInt32);
    INSTANTIATE_NDBUFFER(uint64_t, NDBufferUInt64);

    INSTANTIATE_NDBUFFER(float, NDBufferFloat32);
    INSTANTIATE_NDBUFFER(double, NDBufferFloat64);

#undef INSTANTIATE_NDBUFFER

} // namespace optmath
