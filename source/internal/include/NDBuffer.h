#pragma once
#include "Shape.h"
#include "memory"

namespace optmath {

    template <typename T>
    class NDBuffer {
       private:
        Shape nd_shape;
        std::shared_ptr<T[]> nd_buffer;

       public:
        NDBuffer(const Shape&& shape_) : nd_shape(shape_) {
            nd_buffer = std::make_shared<T[]>(nd_shape.buffer_size());
        }
        const Shape& shape() const { return nd_shape; }
    };

}  // namespace optmath
