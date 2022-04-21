#pragma once
#include <cassert>
#include <initializer_list>
#include <memory>

#include "NDShape.h"

#define NDBUFFER_VAL_T T
#define NDBUFFER_TEMPLATE template <typename NDBUFFER_VAL_T>

namespace optmath {

    NDBUFFER_TEMPLATE
    class NDBuffer {

      private:
        NDShape                           nd_shape;
        std::shared_ptr<NDBUFFER_VAL_T[]> nd_buffer;

      public:
        NDBuffer(const NDShape& shape_)
            : nd_shape(shape_) {
            nd_buffer =
                std::make_shared<NDBUFFER_VAL_T[]>(nd_shape.buffer_size());
        }
        // copy
        NDBuffer(const NDBuffer& other)
            : nd_buffer(other.nd_buffer),
              nd_shape(other.nd_shape) {
            assert(this->buffer_size() == other.buffer_size());
        };
        NDBuffer& operator=(const NDBuffer& other) {
            if (this != &other) {
                this->rebind(other);
                assert(this->buffer_size() == other.buffer_size());
            }
            return *this;
        };

        NDBuffer(NDBuffer&& other);
        NDBuffer& operator=(NDBuffer&& other);

        const NDShape& shape() const;
        std::size_t    buffer_size() const;
        std::size_t    buffer_reference_count() const;
        void           reshape(const NDShape& new_shape);
        void           rebind(const NDBuffer& other);
        void           fill(const NDBUFFER_VAL_T& value);

        NDBUFFER_VAL_T& operator[](const NDIndex& index);
    };

#define EXTERN_NDBUFFER(typename) extern template class NDBuffer<typename>;

    EXTERN_NDBUFFER(int8_t);
    EXTERN_NDBUFFER(int16_t);
    EXTERN_NDBUFFER(int32_t);
    EXTERN_NDBUFFER(int64_t);

    EXTERN_NDBUFFER(uint8_t);
    EXTERN_NDBUFFER(uint16_t);
    EXTERN_NDBUFFER(uint32_t);
    EXTERN_NDBUFFER(uint64_t);

    EXTERN_NDBUFFER(float);
    EXTERN_NDBUFFER(double);

#undef EXTERN_NDBUFFER

} // namespace optmath

#include "NDBuffer.tpp"

#undef NDBUFFER_TEMPLATE
#undef NDBUFFER_VAL_T
