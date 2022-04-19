#pragma once
#include <cassert>
#include <initializer_list>
#include <memory>

#include "NDShape.h"

namespace optmath {

    template <typename T> class NDBuffer {
      private:
        NDShape              nd_shape;
        std::shared_ptr<T[]> nd_buffer;

      public:
        NDBuffer(const NDShape& shape_)
            : nd_shape(shape_) {
            nd_buffer = std::make_shared<T[]>(nd_shape.buffer_size());
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
        // Move in scenario { NDBuffer this = std::move(other); }
        NDBuffer(NDBuffer&& other)
            : nd_buffer(std::move(other.nd_buffer)),
              nd_shape(std::move(other.nd_shape)) {
            assert(other.nd_buffer == nullptr);
            assert(other.nd_shape.size() == 0);
            assert(other.nd_shape.buffer_size() == 0);
        };
        // Move in scenario { this = std::move(other); }
        NDBuffer& operator=(NDBuffer&& other) {
            if (this != &other) {
                this->nd_buffer = std::move(other.nd_buffer);
                this->nd_shape  = std::move(other.nd_shape);
                assert(other.nd_buffer == nullptr);
                assert(other.nd_shape.size() == 0);
                assert(other.nd_shape.buffer_size() == 0);
            }
            return *this;
        }

        // Returns shape of current buffer
        const NDShape& shape() const {
            return nd_shape;
        }
        // Returns total in memory size of buffer.
        std::size_t buffer_size() const {
            return nd_shape.buffer_size();
        }
        // Returns number of active references to underlying buffer
        std::size_t buffer_reference_count() const {
            return nd_buffer.use_count();
        }
        // changes shape of the object without changing buffer
        void reshape(const NDShape& new_shape) {
            assert(new_shape.buffer_size() == nd_shape.buffer_size());
            this->nd_shape = new_shape;
        }
        // Drops reference to old buffer and shares reference from other
        // buffer.
        void rebind(const NDBuffer& other) {
            this->nd_buffer = other.nd_buffer;
            this->nd_shape  = other.nd_shape;
        }
        // Fill buffer with single value.
        void fill(const T& value) {
            std::fill_n(nd_buffer.get(), nd_shape.buffer_size(), value);
        }
        template <typename __T = std::vector<T>>
        void set(const std::vector<__T>& vec) {
            for (auto&& i : vec) {
                set(i);
            }
        }
        void set(const std::vector<T>& vec) {
            for (auto&& i : vec) {}
        }
        // void set(const std::initializer_list<std::initializer_list<T>>&
        // initial_values) {

        // }
        // Access and modify values in buffer.
        T& operator[](const NDIndex& index) {
            assert(index.size() == nd_shape.size());
            return nd_buffer[nd_shape.in_buffer_position(index)];
        }
    };

    extern template class NDBuffer<int8_t>;
    extern template class NDBuffer<int16_t>;
    extern template class NDBuffer<int32_t>;
    extern template class NDBuffer<int64_t>;

    extern template class NDBuffer<uint8_t>;
    extern template class NDBuffer<uint16_t>;
    extern template class NDBuffer<uint32_t>;
    extern template class NDBuffer<uint64_t>;

    extern template class NDBuffer<float>;
    extern template class NDBuffer<double>;

} // namespace optmath
