#include "NDBuffer.h"

namespace optmath {

    template class NDBuffer<int8_t>;
    template class NDBuffer<int16_t>;
    template class NDBuffer<int32_t>;
    template class NDBuffer<int64_t>;

    template class NDBuffer<uint8_t>;
    template class NDBuffer<uint16_t>;
    template class NDBuffer<uint32_t>;
    template class NDBuffer<uint64_t>;

    template class NDBuffer<float>;
    template class NDBuffer<double>;

    using NDBufferInt8  = NDBuffer<int8_t>;
    using NDBufferInt16 = NDBuffer<int16_t>;
    using NDBufferInt32 = NDBuffer<int32_t>;
    using NDBufferInt64 = NDBuffer<int64_t>;

    using NDBufferUInt8  = NDBuffer<uint8_t>;
    using NDBufferUInt16 = NDBuffer<uint16_t>;
    using NDBufferUInt32 = NDBuffer<uint32_t>;
    using NDBufferUInt64 = NDBuffer<uint64_t>;

    using NDBufferFloat32 = NDBuffer<float>;
    using NDBufferFloat64 = NDBuffer<double>;

} // namespace optmath
