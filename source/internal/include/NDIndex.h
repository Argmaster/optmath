#pragma once
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>

namespace optmath {

    using index_t = int64_t;
    using __shape_vector = std::vector<index_t>;

    class NDIndex {
      private:
        __shape_vector nd_value;

      public:
        NDIndex(const std::initializer_list<index_t>& shape_);

        NDIndex(const NDIndex& other);
        NDIndex& operator=(const NDIndex& other);

        NDIndex(NDIndex&& other);
        NDIndex& operator=(NDIndex&& other);

        index_t&    operator[](std::size_t __i);
        std::size_t size() const;

        __shape_vector::iterator               begin();
        __shape_vector::iterator               end();
        __shape_vector::const_iterator         cbegin() const;
        __shape_vector::const_iterator         cend() const;
        __shape_vector::const_reverse_iterator crbegin() const;
        __shape_vector::const_reverse_iterator crend() const;

        friend bool operator==(const NDIndex& lhs, const NDIndex& rhs);
        friend bool operator!=(const NDIndex& lhs, const NDIndex& rhs);
        friend std::ostream& operator<<(std::ostream&  out,
                                        const NDIndex& other);
    };

} // namespace optmath
