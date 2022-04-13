#pragma once
#include <algorithm>
#include <cstdint>
#include <execution>
#include <numeric>

#include "NDIndex.h"

namespace optmath {

    class NDShape : public NDIndex {
       private:
        std::size_t nd_buffer_size;

       public:
        NDShape(const std::initializer_list<int64_t> &shape_)
            : NDIndex(shape_) {
            // calculates and caches minimal buffer size required for this
            // shape
            nd_buffer_size = std::reduce(
                std::execution::par, this->cbegin(), this->cend(), 1,
                [](int64_t first, int64_t second) { return first * second; });
        }
        // total size of buffer required to contain tensor of this shape
        std::size_t buffer_size() const { return nd_buffer_size; }
    };

}  // namespace optmath
