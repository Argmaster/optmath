#pragma once
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <numeric>

#include "NDIndex.h"

namespace optmath {

    using shape_t = index_t;

    class NDShape : public NDIndex {
      private:
        index_t nd_buffer_size;

      protected:
        void _set(index_t, index_t);
        void _calculate_buffer_size();

      public:
        NDShape(const std::initializer_list<shape_t>& shape_);
        NDShape(const std::vector<shape_t>& shape_);
        NDShape() {}

        NDShape(const NDShape& other);
        NDShape& operator=(const NDShape& other);

        NDShape(NDShape&& other);
        NDShape& operator=(NDShape&& other);

        index_t              buffer_size() const;
        index_t              in_buffer_position(const NDIndex& index) const;
        friend std::ostream& operator<<(std::ostream&  out,
                                        const NDShape& other);
    };

} // namespace optmath
