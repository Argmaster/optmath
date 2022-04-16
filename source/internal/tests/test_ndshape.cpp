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

    TEST_F(NDShapeTest, CopyConstruction) {
        auto test_index = optmath::NDShape({2, 1, 4});
        { auto test_index_copy{test_index}; }
        ASSERT_EQ(test_index[0], 2LL);
        ASSERT_EQ(test_index[1], 1LL);
        ASSERT_EQ(test_index[2], 4LL);
    }

    TEST_F(NDShapeTest, CopyAssignment) {
        auto test_index = optmath::NDShape({2, 1, 4});
        {
            optmath::NDShape test_index_copy{3, 3};
            ASSERT_EQ(test_index_copy[0], 3);
            ASSERT_EQ(test_index_copy[1], 3LL);
            test_index_copy = test_index;
            ASSERT_EQ(test_index_copy[0], 2LL);
            ASSERT_EQ(test_index_copy[1], 1LL);
            ASSERT_EQ(test_index_copy[2], 4LL);
        }
        ASSERT_EQ(test_index[0], 2LL);
        ASSERT_EQ(test_index[1], 1LL);
        ASSERT_EQ(test_index[2], 4LL);
    }

    TEST_F(NDShapeTest, MoveConstruction) {
        auto test_index = optmath::NDShape({2, 1, 4});
        { auto test_index_copy{std::move(test_index)}; }
        ASSERT_EQ(test_index[0], 2LL);
        ASSERT_EQ(test_index[1], 1LL);
        ASSERT_EQ(test_index[2], 4LL);
    }

    TEST_F(NDShapeTest, MoveAssignment) {
        auto test_index = optmath::NDShape({2, 1, 4});
        {
            optmath::NDShape test_index_copy{3, 3};
            ASSERT_EQ(test_index_copy[0], 3);
            ASSERT_EQ(test_index_copy[1], 3LL);
            test_index_copy = std::move(test_index);
            ASSERT_EQ(test_index_copy[0], 2LL);
            ASSERT_EQ(test_index_copy[1], 1LL);
            ASSERT_EQ(test_index_copy[2], 4LL);
        }
        ASSERT_EQ(test_index[0], 2LL);
        ASSERT_EQ(test_index[1], 1LL);
        ASSERT_EQ(test_index[2], 4LL);
    }

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
