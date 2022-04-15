#include <gtest/gtest.h>

#include "NDShape.h"

namespace optmath {
    class NDShapeTest : public ::testing::Test {};

    TEST_F(NDShapeTest, NewNDShape) {
        auto test_shape = optmath::NDShape{2, 1, 4};
        ASSERT_EQ(test_shape[0], 2);
        ASSERT_EQ(test_shape[1], 1);
        ASSERT_EQ(test_shape[2], 4);
        ASSERT_EQ(test_shape.size(), 3);
    }
    // TODO Add tests for move and copy

    TEST_F(NDShapeTest, BufferSize3Dims) {
        auto test_shape = optmath::NDShape{2, 1, 4};
        ASSERT_EQ(test_shape.buffer_size(), 8);
    }

    TEST_F(NDShapeTest, BufferSizeTypicalMatrix) {
        auto test_shape = optmath::NDShape{32, 32};
        ASSERT_EQ(test_shape.buffer_size(), 1024);
    }

    TEST_F(NDShapeTest, NoNDShapeAssignment) {
        auto test_shape = optmath::NDShape{32, 32};
        // test_shape[0] = 24; // should be compile error - uncomment for
        // manual check
        ASSERT_EQ(test_shape[0], 32);
        ASSERT_EQ(test_shape[1], 32);
    }

    TEST_F(NDShapeTest, InBufferPosition) {
        auto test_shape = optmath::NDShape{4, 5, 3};
        ASSERT_EQ(test_shape.in_buffer_position({1, 0, 1}), 21);

        auto test_shape_2 = optmath::NDShape{38, 11};
        ASSERT_DEATH(test_shape_2.in_buffer_position({1, 0, 1}), "");
    }

}  // namespace optmath
