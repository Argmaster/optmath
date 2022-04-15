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
        NDBuffer(NDBuffer&&) = delete;
        NDBuffer& operator=(NDBuffer&&) = delete;

        const NDShape& shape() const { return nd_shape; }
        std::size_t buffer_size() const { return nd_shape.buffer_size(); }
        std::size_t buffer_reference_count() const {
            return nd_buffer.use_count();
        }
        void reshape(const NDShape& new_shape) {
            assert(new_shape.buffer_size() == nd_shape.buffer_size());
            this->nd_shape = new_shape;
        }
        void rebind(const NDBuffer& other) {
            this->nd_buffer = other.nd_buffer;
            this->nd_shape = other.nd_shape;
        }
        void resize(const NDShape& new_shape) {
            nd_buffer = std::make_shared<T[]>(nd_shape.buffer_size());
            this->nd_shape = new_shape;
        }
        void fill(const T& value) {
            std::fill_n(nd_buffer.get(), nd_shape.buffer_size(), value);
        }
        T& operator[](const NDIndex& index) {
            assert(index.size() == nd_shape.size());
            return nd_buffer[nd_shape.in_buffer_position(index)];
        }
    };

}  // namespace optmath
