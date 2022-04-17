#pragma once
#include <cassert>
#include <memory>

#include "NDShape.h"

namespace optmath {

    template <typename T>
    class NDBuffer {
       private:
        NDShape nd_shape;
        std::shared_ptr<T[]> nd_buffer;

       public:
        NDBuffer(const NDShape& shape_) : nd_shape(shape_) {
            nd_buffer = std::make_shared<T[]>(nd_shape.buffer_size());
        }
        // copy
        NDBuffer(const NDBuffer&) = delete;
        NDBuffer& operator=(const NDBuffer&) = delete;
        // move
        NDBuffer(NDBuffer&& other)
            : nd_buffer(other.nd_buffer),
              nd_shape(other.nd_shape){};
        NDBuffer& operator=(NDBuffer&& other) {
            if (this != &other) {
                this->nd_buffer = std::move(other.nd_buffer);
                this->nd_shape = std::move(other.nd_shape);
            }
            return *this;
        }

        // Returns shape of current buffer
        const NDShape& shape() const { return nd_shape; }
        // Returns total in memory size of buffer.
        std::size_t buffer_size() const { return nd_shape.buffer_size(); }
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
            this->nd_shape = other.nd_shape;
        }
        // Drops reference to old buffer and creates new one mathing given
        // size.
        void resize(const NDShape& new_shape) {
            nd_buffer = std::make_shared<T[]>(nd_shape.buffer_size());
            this->nd_shape = new_shape;
        }
        void fill(const T& value) {
            std::fill_n(nd_buffer.get(), nd_shape.buffer_size(), value);
        }
        // Access and modify values in buffer.
        T& operator[](const NDIndex& index) {
            assert(index.size() == nd_shape.size());
            return nd_buffer[nd_shape.in_buffer_position(index)];
        }
    };

}  // namespace optmath
