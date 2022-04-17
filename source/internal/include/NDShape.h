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
        // construct from NDShape({a, b, ...})
        NDShape(const std::initializer_list<int64_t> &shape_)
            : NDIndex(shape_) {
            // calculates and caches minimal buffer size required for
            // nd buffer with this shape
            nd_buffer_size = std::reduce(
                std::execution::par, this->cbegin(), this->cend(), 1,
                [](int64_t first, int64_t second) { return first * second; });
        }
        NDShape(const NDShape &other)
            : NDIndex(other) {
            nd_buffer_size = other.nd_buffer_size;
        }
        // Copy underlying std::vector
        NDShape &operator=(const NDShape &other) {
            if (this != &other) {
                this->NDIndex::operator=(other);
                this->nd_buffer_size = other.nd_buffer_size;
            }
            return *this;
        };
        // Move underlying std::vector
        NDShape(NDShape &&other)
            : NDIndex(std::move(other)) {
            nd_buffer_size = other.nd_buffer_size;
            other.nd_buffer_size = 0;
        };
        // Move underlying std::vector
        NDShape &operator=(NDShape &&other) {
            if (this != &other) {
                this->NDIndex::operator=(other);
                this->nd_buffer_size = other.nd_buffer_size;
                other.nd_buffer_size = 0;
            }
            return *this;
        };
        // total size of buffer required to contain tensor of this shape
        std::size_t buffer_size() const { return nd_buffer_size; }
        // Calculates in buffer index of element pointed by NDIndex object.
        std::size_t in_buffer_position(const NDIndex &index) {
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
        // C++ std::out << NDShape(); compatibility
        friend std::ostream &operator<<(std::ostream &out,
                                        const NDShape &other);
    };

}  // namespace optmath
