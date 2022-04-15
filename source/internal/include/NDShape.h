#pragma once
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <execution>
#include <numeric>

#include "NDIndex.h"

namespace optmath {

    class NDShape : public NDIndex {
       private:
        std::size_t nd_buffer_size;

       public:
        NDShape(const std::initializer_list<int64_t>& shape_)
            : NDIndex(shape_) {
            // calculates and caches minimal buffer size required for this
            // shape
            nd_buffer_size = std::reduce(
                std::execution::par, this->cbegin(), this->cend(), 1,
                [](int64_t first, int64_t second) { return first * second; });
        }
        // TODO implement those
        // copy
        // NDShape(const NDShape&) = delete;
        // NDShape& operator=(const NDShape&) = delete;
        // move
        // NDShape(NDShape&&) = delete;
        // NDShape& operator=(NDShape&&) = delete;
        // total size of buffer required to contain tensor of this shape
        std::size_t buffer_size() const { return nd_buffer_size; }
        // Calculates in buffer index of element pointed by NDIndex object.
        std::size_t in_buffer_position(const NDIndex& index) {
            // size inequality is UB
            assert(index.size() == this->size());

            auto beginShape = this->crbegin();
            auto endShape = this->crend();
            auto beginIndex = index.crbegin();
            auto endIndex = index.crend();

            std::size_t position = 0ULL;
            std::size_t multiplier = 1ULL;

            while (beginShape != endShape) {
                position += *beginIndex * multiplier;

                beginShape++;
                beginIndex++;

                multiplier *= *beginShape;
            }
            return position;
        }
    };

}  // namespace optmath
