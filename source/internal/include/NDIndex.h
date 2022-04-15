#pragma once
#include <cstdint>
#include <iostream>
#include <vector>

namespace optmath {

    using __shape_vector = std::vector<int64_t>;

    class NDIndex {
       private:
        __shape_vector nd_shape;

       public:
        NDIndex(const std::initializer_list<int64_t> &shape_)
            : nd_shape(shape_) {}
        // copy
        NDIndex(const NDIndex &other) : nd_shape(other.nd_shape) {}
        NDIndex &operator=(const NDIndex &other) {
            if (this != &other) {
                this->nd_shape = other.nd_shape;
            }
            return *this;
        };
        // move
        // intentionally move creates a copy of shape
        NDIndex(NDIndex &&other) : nd_shape(other.nd_shape){};
        // intentionally move creates a copy of shape
        NDIndex &operator=(NDIndex &&other) {
            if (this != &other) {
                this->nd_shape = other.nd_shape;
            }
            return *this;
        };
        // Index access across dimensions of NDIndex
        int64_t operator[](std::size_t __i) const { return nd_shape[__i]; }
        // number of dimensions
        std::size_t size() const { return nd_shape.size(); }
        // constant forward iterator
        std::vector<int64_t>::const_iterator cbegin() const {
            return nd_shape.cbegin();
        }
        // constant forward iterator
        std::vector<int64_t>::const_iterator cend() const {
            return nd_shape.cend();
        }
        // forward iterator but forced to be const - no in place modifications
        std::vector<int64_t>::const_iterator begin() const {
            return nd_shape.cbegin();
        }
        // forward iterator but forced to be const - no in place modifications
        std::vector<int64_t>::const_iterator end() const {
            return nd_shape.cend();
        }
        // constant reverse iterator
        std::vector<int64_t>::const_reverse_iterator crbegin() const {
            return nd_shape.crbegin();
        }
        // constant reverse iterator
        std::vector<int64_t>::const_reverse_iterator crend() const {
            return nd_shape.crend();
        }
        // only equality/inequality comparisons supported
        // equality checks equality of all index values
        friend bool operator==(const NDIndex &lhs, const NDIndex &rhs);
        friend bool operator!=(const NDIndex &lhs, const NDIndex &rhs);
    };

}  // namespace optmath
