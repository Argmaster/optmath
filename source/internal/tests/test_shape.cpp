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
        ASSERT_EQ(test_shape.buffer_size(), 8);
    }

    TEST_F(ShapeTest, BufferSizeTypicalMatrix) {
        auto test_shape = optmath::Shape{32, 32};
        ASSERT_EQ(test_shape.buffer_size(), 1024);
    }

    TEST_F(ShapeTest, NoShapeAssignment) {
        auto test_shape = optmath::Shape{32, 32};
        // test_shape[0] = 24; // should be compile error - uncomment for
        // manual check
        ASSERT_EQ(test_shape[0], 32);
        ASSERT_EQ(test_shape[1], 32);
    }

    TEST_F(ShapeTest, EqualityCheck) {
        ASSERT_EQ(optmath::Shape({32, 32}), optmath::Shape({32, 32}));
    }
}  // namespace optmath
