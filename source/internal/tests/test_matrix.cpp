#include <gtest/gtest.h>

#include "Matrix.h"

namespace optmath {
    class MatrixTest : public ::testing::Test {};

    TEST_F(MatrixTest, DefaultMatrix) {
        auto mtx = optmath::MatrixF32({2, 2});
    }

}  // namespace optmath
