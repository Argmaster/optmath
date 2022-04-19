#pragma once
#include <cstdint>
#include <initializer_list>
#include <memory>
#include <type_traits>
#include <vector>

#include "NDShape.h"

namespace optmath {

    template <typename primitive> class Matrix {
        const NDShape                shape;
        std::shared_ptr<primitive[]> buffer;

        static_assert(std::is_arithmetic<primitive>::value,
                      "primitive must be a floating point type");

      public:
        Matrix(const NDShape& shape_)
            : shape(shape_) {}

        // information-only function

        // state altering functions

        // calculation functions
    }; // namespace Matrix

    template class Matrix<float>;
    template class Matrix<double>;

    using MatrixF32 = optmath::Matrix<float>;
    using MatrixF64 = optmath::Matrix<double>;

} // namespace optmath
