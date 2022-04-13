#pragma once
#include <algorithm>
#include <cstdint>
#include <execution>
#include <numeric>
#include <vector>

namespace optmath {

    using __shape_vector = std::vector<int64_t>;
    class NDShape {
       private:
        __shape_vector shape;
        std::size_t nd_buffer_size;

       public:
        NDShape(const std::initializer_list<int64_t> &shape_) : shape(shape_) {
            nd_buffer_size = std::reduce(
                std::execution::seq, this->cbegin(), this->cend(), 1,
                [](int64_t first, int64_t second) { return first * second; });
        }

        std::size_t buffer_size() const { return nd_buffer_size; }
        int64_t operator[](std::size_t __i) const { return shape[__i]; }

        std::size_t size() const { return shape.size(); }
        std::vector<int64_t>::const_iterator cbegin() const {
            return shape.cbegin();
        }
        std::vector<int64_t>::const_iterator cend() const {
            return shape.cend();
        }

        friend bool operator==(const NDShape &lhs, const NDShape &rhs);
        friend bool operator!=(const NDShape &lhs, const NDShape &rhs);
    };

    bool operator==(const NDShape &lhs, const NDShape &rhs) {
        if (lhs.size() == rhs.size()) {
            auto lhsb = lhs.cbegin();
            auto rhsb = rhs.cbegin();
            auto lhse = lhs.cend();
            auto rhse = rhs.cend();

            while (lhsb != lhse && rhsb != rhse) {
                auto left = *lhsb;
                auto right = *rhsb;
                if (left != right) return false;
                lhsb++;
                rhsb++;
            }
            return true;
        }
        return false;
    }

    bool operator!=(const NDShape &lhs, const NDShape &rhs) {
        return !(lhs == rhs);
    }

}  // namespace optmath
