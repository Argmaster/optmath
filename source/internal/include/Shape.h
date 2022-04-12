#pragma once
#include <algorithm>
#include <cstdint>
#include <execution>
#include <numeric>
#include <vector>

namespace optmath {

    using __shape_vector = std::vector<int64_t>;

    class Shape : private __shape_vector {
       public:
        Shape(const std::initializer_list<int64_t>& shape_)
            : __shape_vector(shape_) {}

        int64_t shape_size() const {
            return std::reduce(
                std::execution::seq, this->cbegin(), this->cend(), 1,
                [](int64_t first, int64_t second) { return first * second; });
        }
        using __shape_vector::size;
        using __shape_vector::operator[];
    };
}  // namespace optmath
