#pragma once
#include <cstdint>
#include <vector>

namespace optmath {

    using __shape_vector = std::vector<int64_t>;

    class NDIndex {
       private:
        __shape_vector shape;

       public:
        NDIndex(const std::initializer_list<int64_t> &shape_)
            : shape(shape_) {}
        int64_t operator[](std::size_t __i) const { return shape[__i]; }
        std::size_t size() const { return shape.size(); }
        // all iterators constant - no in place modifications allowed
        std::vector<int64_t>::const_iterator cbegin() const {
            return shape.cbegin();
        }
        std::vector<int64_t>::const_iterator cend() const {
            return shape.cend();
        }
        std::vector<int64_t>::const_iterator begin() const {
            return shape.cbegin();
        }
        std::vector<int64_t>::const_iterator end() const {
            return shape.cend();
        }
        // only equality/inequality comparisons supported
        // equality checks equality of all index values
        friend bool operator==(const NDIndex &lhs, const NDIndex &rhs);
        friend bool operator!=(const NDIndex &lhs, const NDIndex &rhs);
    };

}  // namespace optmath
