#pragma once
#include <cstdint>
#include <iostream>
#include <vector>

namespace optmath {

    using __shape_vector = std::vector<int64_t>;

    class NDIndex {
       private:
        __shape_vector nd_value;

       public:
        NDIndex(const std::initializer_list<int64_t> &shape_)
            : nd_value(shape_) {}
        // Copy underlying std::vector
        NDIndex(const NDIndex &other) : nd_value(other.nd_value) {}
        // Copy underlying std::vector
        NDIndex &operator=(const NDIndex &other) {
            if (this != &other) {
                this->nd_value = other.nd_value;
            }
            return *this;
        };
        // Move underlying std::vector
        NDIndex(NDIndex &&other) : nd_value(std::move(other.nd_value)){};
        // Move underlying std::vector
        NDIndex &operator=(NDIndex &&other) {
            if (this != &other) {
                this->nd_value = std::move(other.nd_value);
            }
            return *this;
        };
        // Index access across dimensions of NDIndex
        int64_t operator[](std::size_t __i) const { return nd_value[__i]; }
        // number of dimensions
        std::size_t size() const { return nd_value.size(); }
        // constant forward iterator
        __shape_vector::const_iterator cbegin() const {
            return nd_value.cbegin();
        }
        // constant forward iterator
        __shape_vector::const_iterator cend() const { return nd_value.cend(); }
        // forward iterator but forced to be const - no in place modifications
        __shape_vector::const_iterator begin() const {
            return nd_value.cbegin();
        }
        // forward iterator but forced to be const - no in place modifications
        __shape_vector::const_iterator end() const { return nd_value.cend(); }
        // constant reverse iterator
        __shape_vector::const_reverse_iterator crbegin() const {
            return nd_value.crbegin();
        }
        // constant reverse iterator
        __shape_vector::const_reverse_iterator crend() const {
            return nd_value.crend();
        }
        // Check equality of size and all dimensions of nd_index
        friend bool operator==(const NDIndex &lhs, const NDIndex &rhs);
        // Check inequality of size or any dimensions of nd_index
        friend bool operator!=(const NDIndex &lhs, const NDIndex &rhs);
    };

}  // namespace optmath
