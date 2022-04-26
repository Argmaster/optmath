#pragma once
#include <cassert>
#include <initializer_list>
#include <memory>

#include "NDShape.h"

#define NDBUFFER_VAL_T __ndbuffer_val_T
#define NDBUFFER_TEMPLATE template <typename NDBUFFER_VAL_T>

namespace optmath {

    NDBUFFER_TEMPLATE
    class NDBuffer {

      private:
        NDShape                           nd_shape;
        std::unique_ptr<NDBUFFER_VAL_T[]> nd_buffer;

      public:
        NDBuffer(const NDShape& shape_);
        NDBuffer();
        // copy
        NDBuffer(const NDBuffer& other);
        NDBuffer& operator=(const NDBuffer& other);

        NDBuffer(NDBuffer&& other);
        NDBuffer& operator=(NDBuffer&& other);

        const NDShape& shape() const;
        index_t        buffer_size() const;
        void           reshape(const NDShape& new_shape);
        void           fill(const NDBUFFER_VAL_T& value);

        std::ostream& to_stream(std::ostream& stream) const;

        NDBUFFER_VAL_T* begin();
        NDBUFFER_VAL_T* end();

        const NDBUFFER_VAL_T* cbegin() const;
        const NDBUFFER_VAL_T* cend() const;

        NDBUFFER_VAL_T&       operator[](const NDIndex& index);
        const NDBUFFER_VAL_T& operator[](const NDIndex& index) const;
        bool                  operator==(const NDBuffer& other) const;

        friend std::ostream&
        operator<<(std::ostream& out, const NDBuffer<NDBUFFER_VAL_T>& other) {
            other.to_stream(out);
            return out;
        }
    };

#define EXTERN_NDBUFFER(typename, alias)                                      \
    extern template class NDBuffer<typename>;                                 \
    using alias = NDBuffer<typename>;

    EXTERN_NDBUFFER(int8_t, NDBufferInt8);
    EXTERN_NDBUFFER(int16_t, NDBufferInt16);
    EXTERN_NDBUFFER(int32_t, NDBufferInt32);
    EXTERN_NDBUFFER(int64_t, NDBufferInt64);

    EXTERN_NDBUFFER(uint8_t, NDBufferUInt8);
    EXTERN_NDBUFFER(uint16_t, NDBufferUInt16);
    EXTERN_NDBUFFER(uint32_t, NDBufferUInt32);
    EXTERN_NDBUFFER(uint64_t, NDBufferUInt64);

    EXTERN_NDBUFFER(float, NDBufferFloat32);
    EXTERN_NDBUFFER(double, NDBufferFloat64);

#undef EXTERN_NDBUFFER

} // namespace optmath

#include "NDBuffer.tpp"

#undef NDBUFFER_TEMPLATE
#undef NDBUFFER_VAL_T
