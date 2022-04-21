#pragma once

#include "NDBuffer.h"

#define NDBUFFER_METHOD(return_type)                                          \
    NDBUFFER_TEMPLATE return_type NDBuffer<NDBUFFER_VAL_T>::

#define NDBUFFER_T NDBuffer<NDBUFFER_VAL_T>

namespace optmath {
    /**
     * @brief Construct a new NDBuffer object by moving other.
     *
     * @param other object to take ownership from
     */
    NDBUFFER_METHOD()
    NDBuffer(NDBUFFER_T&& other)
        : nd_buffer(std::move(other.nd_buffer)),
          nd_shape(std::move(other.nd_shape)) {
        assert(other.nd_buffer == nullptr);
        assert(other.nd_shape.size() == 0);
        assert(other.nd_shape.buffer_size() == 0);
    };
    /**
     * @brief Move existing object into another one.
     *
     * @param other object to take ownership from
     * @return NDBuffer&
     */
    NDBUFFER_METHOD(NDBUFFER_T&) operator=(NDBUFFER_T&& other) {
        if (this != &other) {
            this->nd_buffer = std::move(other.nd_buffer);
            this->nd_shape  = std::move(other.nd_shape);
            assert(other.nd_buffer == nullptr);
            assert(other.nd_shape.size() == 0);
            assert(other.nd_shape.buffer_size() == 0);
        }
        return *this;
    }
    /**
     * @brief Return current shape of buffer.
     *
     * @return const NDShape&
     */
    NDBUFFER_METHOD(const NDShape&) shape() const {
        return nd_shape;
    }
    /**
     * @brief Returns total (linear) in memory size of buffer.
     *
     * @return std::size_t buffer size
     */
    NDBUFFER_METHOD(std::size_t) buffer_size() const {
        return nd_shape.buffer_size();
    }
    /**
     * @brief Returns number of active references to underlying buffer.
     *
     * @return std::size_t ref count
     */
    NDBUFFER_METHOD(std::size_t) buffer_reference_count() const {
        return nd_buffer.use_count();
    }
    /**
     * @brief Assign new shape without changing buffer.
     *
     */
    NDBUFFER_METHOD(void) reshape(const NDShape& new_shape) {
        assert(new_shape.buffer_size() == this->nd_shape.buffer_size());
        this->nd_shape = new_shape;
    }
    /**
     * @brief Drops reference to old buffer and shares reference from other
     * buffer.
     *
     * @param other buffer to share memory reference from.
     */
    NDBUFFER_METHOD(void) rebind(const NDBuffer& other) {
        this->nd_buffer = other.nd_buffer;
        this->nd_shape  = other.nd_shape;
    }
    /**
     * @brief Fill buffer with single value.
     *
     * @param value
     */
    NDBUFFER_METHOD(void) fill(const NDBUFFER_VAL_T& value) {
        std::fill_n(nd_buffer.get(), nd_shape.buffer_size(), value);
    }
    /**
     * @brief Access single element from buffer.
     *
     * @param index n-dimensional index pointing to element
     * @return T& in buffer element reference
     */
    NDBUFFER_METHOD(NDBUFFER_VAL_T&) operator[](const NDIndex& index) {
        assert(index.size() == nd_shape.size());
        return nd_buffer[nd_shape.in_buffer_position(index)];
    }
} // namespace optmath

#undef NDBUFFER_METHOD
#undef NDBUFFER_T
