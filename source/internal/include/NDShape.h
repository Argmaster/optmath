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
        NDShape(const std::initializer_list<int64_t>& shape_);

        NDShape(const NDShape& other);
        NDShape& operator=(const NDShape& other);

        NDShape(NDShape&& other);
        NDShape& operator=(NDShape&& other);

        std::size_t          buffer_size() const;
        std::size_t          in_buffer_position(const NDIndex& index);
        friend std::ostream& operator<<(std::ostream&  out,
                                        const NDShape& other);
    };

} // namespace optmath
