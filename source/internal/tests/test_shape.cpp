#include <gtest/gtest.h>

#include "Shape.h"

namespace optmath {
    class ShapeTest : public ::testing::Test {};

    TEST_F(ShapeTest, NewShape) {
        auto test_shape = optmath::Shape{2, 1, 4};
        ASSERT_EQ(test_shape[0], 2);
        ASSERT_EQ(test_shape[1], 1);
        ASSERT_EQ(test_shape[2], 4);
        ASSERT_EQ(test_shape.size(), 3);
    }

    TEST_F(ShapeTest, BufferSize) {
        auto test_shape = optmath::Shape{2, 1, 4};
        ASSERT_EQ(test_shape.shape_size(), 8);
    }

}  // namespace optmath
