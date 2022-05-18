#pragma once

#include "NDBuffer.h"

#define NDBUFFER_METHOD(return_type)                                          \
    NDBUFFER_TEMPLATE return_type NDBuffer<NDBUFFER_VAL_T>::

#define NDBUFFER_T NDBuffer<NDBUFFER_VAL_T>

namespace optmath {
    /**
     * @brief Construct a new NDBuffer object
     *
     * @param shape_ shape of buffer to create.
     */
    NDBUFFER_METHOD()
    NDBuffer(const NDShape& shape_)
        : nd_shape(shape_) {
        auto size = shape_.buffer_size();
        assert(size != 0);
        nd_buffer = std::make_unique<NDBUFFER_VAL_T[]>(size);
        assert(this->nd_buffer != nullptr);
    }
    /**
     * @brief Construct a new NDBuffer object without initialization.
     *
     * @param shape_ shape of buffer to create.
     */
    NDBUFFER_METHOD()
    NDBuffer() {}
    /**
     * @brief Construct a new NDBuffer object
     *
     * @param other buffer to copy
     */
    NDBUFFER_METHOD()
    NDBuffer(const NDBUFFER_T& other)
        : nd_shape(other.nd_shape) {
        assert(other.nd_buffer != nullptr);

        auto size       = other.buffer_size();
        this->nd_buffer = std::make_unique<NDBUFFER_VAL_T[]>(size);

        assert(this->nd_buffer != nullptr);
        assert(this->buffer_size() == other.buffer_size());

        std::copy(other.cbegin(), other.cend(), this->begin());

        assert(this->nd_buffer != nullptr);
    };
    /**
     * @brief Share reference to another buffer.
     *
     * @param other
     * @return NDBuffer&
     */
    NDBUFFER_METHOD(NDBUFFER_T&) operator=(const NDBuffer& other) {
        if (this != &other) {
            assert(other.nd_buffer != nullptr);

            this->nd_shape  = other.shape();
            auto size       = other.buffer_size();
            this->nd_buffer = std::make_unique<NDBUFFER_VAL_T[]>(size);

            assert(this->nd_buffer != nullptr);
            assert(this->buffer_size() == other.buffer_size());

            std::copy(other.cbegin(), other.cend(), this->begin());

            assert(this->nd_buffer != nullptr);
        }
        return *this;
    };
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
        assert(this->nd_buffer != nullptr);
    };
    /**
     * @brief Move existing object into another one.
     *
     * @param other object to take ownership from
     * @return NDBuffer&
     */
    NDBUFFER_METHOD(NDBUFFER_T&) operator=(NDBUFFER_T&& other) {
        assert(other.nd_buffer != nullptr);
        if (this != &other) {
            this->nd_buffer = std::move(other.nd_buffer);
            this->nd_shape  = std::move(other.nd_shape);
            assert(other.nd_buffer == nullptr);
            assert(this->nd_buffer != nullptr);
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
     * @return index_t buffer size
     */
    NDBUFFER_METHOD(index_t) buffer_size() const {
        assert(this->nd_buffer != nullptr);
        return nd_shape.buffer_size();
    }
    /**
     * @brief Assign new shape without changing buffer.
     *
     */
    NDBUFFER_METHOD(void) reshape(const NDShape& new_shape) {
        assert(this->nd_buffer != nullptr);
        assert(new_shape.buffer_size() == this->buffer_size());
        this->nd_shape = new_shape;
    }
    /**
     * @brief Fill buffer with single value.
     *
     * @param value
     */
    NDBUFFER_METHOD(void) fill(const NDBUFFER_VAL_T& value) {
        assert(this->nd_buffer != nullptr);
        std::fill(this->begin(), this->end(), value);
    }
    /**
     * @brief Return begin iterator for buffer.
     *
     * @return NDBUFFER_VAL_T*
     */
    NDBUFFER_METHOD(NDBUFFER_VAL_T*) begin() {
        assert(this->nd_buffer != nullptr);
        return this->nd_buffer.get();
    }
    /**
     * @brief Return end iterator sentinel for buffer.
     *
     * @return NDBUFFER_VAL_T*
     */
    NDBUFFER_METHOD(NDBUFFER_VAL_T*) end() {
        assert(this->nd_buffer != nullptr);
        return this->nd_buffer.get() + this->buffer_size();
    }
    /**
     * @brief Return constant begin iterator for buffer.
     *
     * @return const NDBUFFER_VAL_T*
     */
    NDBUFFER_METHOD(const NDBUFFER_VAL_T*) cbegin() const {
        assert(this->nd_buffer != nullptr);
        return this->nd_buffer.get();
    }
    /**
     * @brief Return constant end iterator sentinel for buffer.
     *
     * @return const NDBUFFER_VAL_T*
     */
    NDBUFFER_METHOD(const NDBUFFER_VAL_T*) cend() const {
        assert(this->nd_buffer != nullptr);
        return this->nd_buffer.get() + this->buffer_size();
    }
    /**
     * @brief Access single element from buffer.
     *
     * @param index n-dimensional index pointing to element
     * @return T& in buffer element reference
     */
    NDBUFFER_METHOD(NDBUFFER_VAL_T&) operator[](const NDIndex& nd_indexer) {
        assert(this->nd_buffer != nullptr);
        assert(nd_indexer.size() == nd_shape.size());
        auto index = nd_shape.in_buffer_position(nd_indexer);
        assert(index < this->buffer_size());
        assert(index >= 0);
        return nd_buffer[index];
    }
    /**
     * @brief Access single element from buffer.
     *
     * @param index n-dimensional index pointing to element
     * @return T& in buffer element reference
     */
    NDBUFFER_METHOD(const NDBUFFER_VAL_T&)
    operator[](const NDIndex& nd_indexer) const {
        assert(this->nd_buffer != nullptr);
        assert(nd_indexer.size() == nd_shape.size());
        auto index = nd_shape.in_buffer_position(nd_indexer);
        assert(index < this->buffer_size());
        assert(index >= 0);
        return nd_buffer[index];
    }
    /**
     * @brief Compare two NDBuffer instances.
     *
     * @param other
     * @return true for identical buffer or same buffer.
     */
    NDBUFFER_METHOD(bool) operator==(const NDBuffer& other) const {
        if (this == &other)
            return true;
        if (this->nd_shape != other.nd_shape)
            return false;
        return std::equal(this->cbegin(), this->cend(), other.cbegin(),
                          other.cend());
    }
    /**
     * @brief C++ std::out << NDBuffer(); compatibility.
     *
     * @param out stream to write to
     * @param other buffer to stringify
     * @return std::ostream& stream for chaining
     */
    NDBUFFER_METHOD(std::ostream&) to_stream(std::ostream& stream) const {
        assert(this->nd_buffer != nullptr);
        auto begin = this->cbegin();
        auto end   = this->cend();

        stream << '[';

        while (true) {
            stream << *begin;
            begin++;
            if (begin == end) {
                break;
            }
            stream << ',' << ' ';
        }
        stream << ']';

        return stream;
    }
} // namespace optmath

#undef NDBUFFER_METHOD
#undef NDBUFFER_T
