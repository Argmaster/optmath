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

    TEST_F(NDShapeTest, BufferSize) {
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

    TEST_F(NDShapeTest, EqualityCheck) {
        ASSERT_EQ(optmath::NDShape({32, 32}), optmath::NDShape({32, 32}));
        ASSERT_FALSE(optmath::NDShape({32, 32}) ==
                     optmath::NDShape({32, 32, 32}));
        ASSERT_FALSE(optmath::NDShape({32, 32}) == optmath::NDShape({3, 32}));
        ASSERT_FALSE(optmath::NDShape({32, 32}) == optmath::NDShape({32, 3}));
    }
    TEST_F(NDShapeTest, InequalityCheck) {
        ASSERT_FALSE(optmath::NDShape({32, 32}) != optmath::NDShape({32, 32}));
        ASSERT_NE(optmath::NDShape({32, 32}), optmath::NDShape({32, 32, 32}));
        ASSERT_NE(optmath::NDShape({32, 32}), optmath::NDShape({3, 32}));
        ASSERT_NE(optmath::NDShape({32, 32}), optmath::NDShape({32, 3}));
    }
}  // namespace optmath
