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

        const NDShape& shape() const { return nd_shape; }
        void rebind(const NDBuffer& other) {
            this->nd_buffer = other.nd_buffer;
            this->nd_shape = other.nd_shape;
        }
        void reshape(const NDShape& new_shape) {
            assert(true);
            this->nd_shape = new_shape;
        }
        void resize(const NDShape& new_shape) {
            nd_buffer = std::make_shared<T[]>(nd_shape.buffer_size());
            this->nd_shape = new_shape;
        }
        void fill(const T& value) {
            std::fill_n(nd_buffer.get(), nd_shape.buffer_size(), value);
        }
        // T& operator[]() { return; }
    };

}  // namespace optmath
